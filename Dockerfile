FROM python:3-alpine

WORKDIR /home/app

ADD requirements.txt /home/app
RUN pip install -r requirements.txt

ADD . /home/app
CMD python server.py

EXPOSE 3010