#!/bin/sh

cd $APP_DIR
mkdir ics json
./server & # >> /home/go.log
tail -f /dev/null