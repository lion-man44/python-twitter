#FROM mysql/mysql-server:latest
FROM python:3.9.7-slim

WORKDIR /python


RUN apt-get update -y && \
    apt-get install -y \
      python \
      default-mysql-client
RUN pip install \
      flask \
      flask-sqlalchemy

ADD ./ ./
