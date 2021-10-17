#!/bin/sh
#fix link-count, as cron is being a pain, and docker is making hardlink count >0 (very high)
# touch /etc/crontab /etc/cron.*/*

cd $APP_DIR
./server & # >> /home/go.log
echo "25 8,16 * * * python3 $APP_DIR/cron_task/cron.py >> /home/cron.log 2>&1" >> /etc/cron.d/python-cron
crontab /etc/cron.d/python-cron
echo "[INFO] Python now initializing..."
python3 ./cron_task/cron.py # >> /home/cron.log 2>&1
echo "[INFO] Cron as foreground..."
cron -f
# service cron start
# /bin/bash