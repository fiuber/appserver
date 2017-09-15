FROM ubuntu:trusty

MAINTAINER Fi Uba "fi@uba.ar"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

# install requirements
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# add source files
COPY . /app

ENV HOME=/app


ENV FLASK_APP=server.py

EXPOSE 5000
RUN ["chmod", "+x" , "/app/exec.sh"]


CMD ["/app/exec.sh"]
