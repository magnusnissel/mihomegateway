"""
Logic for reading the gateway data adapted from https://github.com/fcuiller/xiaomi-get-temperature
"""
from socket import socket, AF_INET, SOCK_DGRAM, INADDR_ANY, inet_aton, IPPROTO_IP, IP_ADD_MEMBERSHIP
import struct
import json
import datetime
import os
import asyncio
import aioredis

MULTICAST_GRP = '224.0.0.50'
UDP_PORT = 9898
SOCKET_BUFSIZE = 1024
SOCKET_TIMEOUT = 30


async def main():
    redis_uri = os.environ.get("REDIS_URI", None)
    redis_pw = os.environ.get("REDIS_PW", None)
    if redis_uri is None:
        redis_uri = "redis://localhost:6379/0"
        print("Defaulting to redis://localhost:6379/0")
        print("Set REDIS_URI (and if needed: REDIS_PW) environment variables to specify a different instance")
    pool = await aioredis.create_pool(redis_uri, password=redis_pw)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', UDP_PORT))
    group = inet_aton(MULTICAST_GRP)
    mreq = struct.pack('4sL', group, INADDR_ANY)
    sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
    while True:
        data, addr = sock.recvfrom(SOCKET_BUFSIZE)
        ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        msg = data.decode('utf-8')
        data = json.loads(msg)
        states = json.loads(data["data"])
        for k, v in states.items():
            s = {
                "model": data["model"],
                "sid": data["sid"],
                "short_id": data["short_id"],
                "cmd": data["cmd"],
                "ts": ts,
                "att": k,
                "val": v,
            }
            try:
                s["token"] = data["token"]
            except KeyError:
                pass
            print(s["ts"], s["sid"], s["model"], s["att"], s["val"], sep="\t")
            await pool.execute("lpush", "mihome:incoming", json.dumps(s))
    sock.close()
    pool.close()
    await pool.wait_closed()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())