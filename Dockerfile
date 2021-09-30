FROM python:3.9.7-slim

WORKDIR /python

RUN pip install \
      flask \
      flask-sqlalchemy

ADD ./ ./
