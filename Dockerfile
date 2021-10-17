FROM golang:1.17-buster AS builder

COPY go_src/ ./src

WORKDIR /go/src/server

RUN go mod download && \
    go mod verify && \
    CGO_ENABLED=0 go build -ldflags '-s -w --extldflags "-static -fpic"'

FROM debian:buster-slim

ENV APP_DIR /home

RUN echo "deb http://mirrors.cqu.edu.cn/debian buster main" > /etc/apt/sources.list && \
    apt update && \
    apt upgrade -y && \
    apt install python3 python3-pip cron -y --no-install-recommends && \
    pip3 config set global.index-url https://mirrors.cqu.edu.cn/pypi/web/simple && \
    apt clean

# Debug only
RUN apt install vim procps -y --no-install-recommends && \
    apt clean

COPY ./cron_task/ $APP_DIR/cron_task
# not allowed
# COPY ./credentials/ $APP_DIR/credentials

RUN cd $APP_DIR && \
    pip3 install -r cron_task/requirements.txt
    # python3 cron_task/cron.py

COPY ./cron.sh $APP_DIR/cron_task/
COPY --from=builder ./go/src/server/server $APP_DIR/

EXPOSE 8080

WORKDIR $APP_DIR

CMD ["./cron_task/cron.sh"]