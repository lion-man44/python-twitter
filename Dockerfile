#FROM mysql/mysql-server:latest
FROM python:3.9.7-slim

WORKDIR /python


RUN apt-get update -y && \
    apt-get install -y \
      python \
      default-mysql-client \
      python3-dev \
      default-libmysqlclient-dev \
      build-essential
RUN pip install \
      flask \
      flask-sqlalchemy \
      mysqlclient \
      boto3

ADD ./ ./
