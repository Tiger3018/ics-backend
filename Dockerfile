FROM nginx:latest

RUN echo "deb http://mirrors.cqu.edu.cn/debian buster main" > /etc/apt/sources.list && \
    apt update && \
    apt upgrade -y && \
    apt install python3 python3-pip -y --no-install-recommends && \
    pip3 config set global.index-url https://mirrors.cqu.edu.cn/pypi/web/simple && \
    apt clean

# Debug only
RUN apt install vim -y --no-install-recommends && \
    apt clean

COPY ./cron_task/ /var/cron_task
COPY ./credentials/ /var/credentials

RUN cd /var && \
    pip3 install -r cron_task/requirements.txt && \
    python3 cron_task/cron.py && \
    cp ics/* /usr/share/nginx/html/