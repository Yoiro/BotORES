FROM ubuntu:trusty
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

MAINTAINER Simon De Greve <degrevesim@gmail.com>

RUN apt-get -y update
RUN apt-get install -y -q software-properties-common wget
RUN add-apt-repository -y ppa:mozillateam/firefox-next

RUN mkdir /volume1/
RUN sudo mkdir /volume1/share/
ENV DIRPATH /volume1/share

WORKDIR $DIRPATH

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get update -y
RUN apt-get install -y -q firefox xorg xvfb xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.16.1/geckodriver-v0.16.1-linux64.tar.gz
RUN tar zxvf geckodriver-v0.16.1-linux64.tar.gz -C $DIRPATH/

ADD download_ores.py $DIRPATH/download_ores.py
ADD credentials.json $DIRPATH/credentials.json
ADD crontab $DIRPATH/crontab
ADD requirements.txt $DIRPATH/requirements.txt
ADD __init__.py $DIRPATH/__init__.py

RUN mkdir $DIRPATH/BotDownloads

VOLUME $DIRPATH/BotDownloads

RUN pip install -r requirements.txt

EXPOSE 80 443