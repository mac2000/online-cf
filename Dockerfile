FROM python:alpine

RUN pip install redis
ENV redis=redis
ADD . /code
COPY . /code
