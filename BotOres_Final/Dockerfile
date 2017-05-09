FROM python:3.6

MAINTAINER Simon De Greve - Bury Victor

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

chmod a+x crontab

RUN mkdir $DIRPATH/BotDownloads

RUN pip install -r requirements.txt

RUN cron crontab

VOLUME $DIRPATH

EXPOSE 80 443
