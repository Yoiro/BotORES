FROM python:3.6
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

MAINTAINER Simon De Greve <degrevesim@gmail.com>

RUN apt-get -y update
RUN apt-get install -y -q software-properties-common wget
RUN add-apt-repository -y ppa:mozillateam/firefox-next