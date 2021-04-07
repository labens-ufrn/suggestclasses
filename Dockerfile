# Base Image
FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /code
COPY requirements.txt /code/
ADD . /code/

RUN apt-get update && apt-get upgrade -y && \
    apt-get install python3-dev default-libmysqlclient-dev -y
RUN pip install -r requirements.txt

