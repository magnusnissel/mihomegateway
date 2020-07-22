# mihomegateway

##About
Read data from the Xiaomi Mi Smart Home Gateway and send it to a Redis instance. 
The worker will listen to heartbeat and report data sent by all compatible gateways on the network and split their data values into individual json objects and push them into a Redis list (_mihome:incoming_) for further processing by other services.


An original gateway heartbeat of 

```
{'cmd': 'heartbeat', 'model': 'gateway', 'sid': '[REDACTED]', 'short_id': '0', 'token': 'KUsKFj3RxiJOMgmR', 'data': '{"ip":"192.168.178.25"}'}
```

will get pushed as
```
{'model': 'gateway', 'sid': '[REDACTED]', 'short_id': '0', 'cmd': 'heartbeat', 'ts': '2020-07-22T20:02:40', 'att': 'ip', 'val': '192.168.178.25', 'token': 'KUsKFj3RxiJOMgmR'}
```

Similarly, the hearbeat of an Aquara open/close sensor with two attribute-value pairs (voltage & status) will get split up:

```
{'cmd': 'heartbeat', 'model': 'sensor_magnet.aq2', 'sid': '158d00016c40ff', 'short_id': 53267, 'data': '{"voltage":3055,"status":"close"}'}
```

```
{'model': 'sensor_magnet.aq2', 'sid': '158d00016c40ff', 'short_id': 53267, 'cmd': 'heartbeat', 'ts': '2020-07-22T20:04:36', 'att': 'voltage', 'val': 3055}
{'model': 'sensor_magnet.aq2', 'sid': '158d00016c40ff', 'short_id': 53267, 'cmd': 'heartbeat', 'ts': '2020-07-22T20:04:36', 'att': 'status', 'val': 'close'}
```

## Kudos
I have adapted the core logic for reading the UDP multicast from https://github.com/fcuiller/xiaomi-get-temperature

## Example

Assuming you have Redis using on localhost with the default configuration (_redis://localhost:6379/0_) you can use the following commands to build and then run the image:

```
docker build -t mhgw .
```

```
docker run -t --network host --restart unless-stopped mhgw
```

To specify a different Redis instance / configuration, you can pass the environment variables _REDIS_URI_ & _REDIS_PW_. Depending on your setup you may also need to tweak the network settings. 


