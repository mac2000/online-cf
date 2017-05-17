FROM python:alpine

RUN pip install redis

ADD . /code
COPY . /code
