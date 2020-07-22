FROM python:3.8
COPY requirements.txt /srv
WORKDIR /srv
RUN pip install -r requirements.txt
COPY fetch.py /srv/

CMD ["python", "-u",  "fetch.py"]