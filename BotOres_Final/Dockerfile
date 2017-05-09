FROM ubuntu:latest

MAINTAINER Simon De Greve - Bury Victor

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip cron vim

RUN mkdir /volume1/
RUN mkdir /volume1/share/

ENV DIRPATH /volume1/share
WORKDIR $DIRPATH

ADD download_ores.py $DIRPATH/download_ores.py

RUN chmod a+x download_ores.py

ADD credentials.json $DIRPATH/credentials.json

ADD requirements.txt $DIRPATH/requirements.txt

ADD __init__.py $DIRPATH/__init__.py

ADD crontab $DIRPATH/crontab

RUN chmod a+x crontab

ADD startOresBot.sh $DIRPATH/startOresBot.sh

RUN mkdir $DIRPATH/BotDownloads

RUN pip3 install -U pip

RUN pip3 install -r requirements.txt

RUN crontab -u root crontab

EXPOSE 80 443
