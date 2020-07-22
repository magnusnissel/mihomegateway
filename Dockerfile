FROM python:3.8
COPY requirements.txt /srv
WORKDIR /srv
RUN pip install -r requirements.txt
COPY worker.py /srv/

CMD ["python", "-u",  "worker.py"]