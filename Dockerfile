FROM ubuntu:xenial

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3 python3-pip python3-lxml python3-cssutils libxml2-dev libxslt1-dev inkscape libav-tools
RUN apt-get install -y zlib1g-dev

ADD . /app
WORKDIR /app

RUN pip3 install -r requirements.txt