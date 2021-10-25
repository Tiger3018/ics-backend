#!/bin/sh
#fix link-count, as cron is being a pain, and docker is making hardlink count >0 (very high)
# touch /etc/crontab /etc/cron.*/*

cd $APP_DIR
./server & # >> /home/go.log
mkdir /etc/cron.d -p
echo "25 14 2,5 * * python3 $APP_DIR/pytask/cron.py >> /home/cron.log 2>&1" >> /etc/cron.d/python-cron
crontab /etc/cron.d/python-cron
echo "[INFO] Python now initializing..."
python3 ./pytask/cron.py # >> /home/cron.log 2>&1
echo "[INFO] Cron as foreground..."
supercronic /etc/cron.d/python-cron
# service cron start
# /bin/bash