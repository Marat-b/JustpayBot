FROM python:3.10.12-slim
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN mkdir app
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY . /app
