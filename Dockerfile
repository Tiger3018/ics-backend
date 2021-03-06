FROM golang:1.17-buster AS builder

COPY go_src/ ./src

WORKDIR /go/src/server

RUN go mod download && \
    go mod verify && \
    CGO_ENABLED=0 go build -ldflags '-s -w --extldflags "-static -fpic"'

FROM debian:buster-slim

ENV APP_DIR /home
ENV PORT 2021
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.12/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=048b95b48b708983effb2e5c935a1ef8483d9e3e

# Fallback for container without internet access
# RUN echo "deb http://mirrors.cqu.edu.cn/debian buster main" > /etc/apt/sources.list && \
#   apt update && \
RUN apt update && \
    apt upgrade -y && \
    apt install python3 python3-pip curl -y --no-install-recommends && \
    # pip3 config set global.index-url https://mirrors.cqu.edu.cn/pypi/web/simple && \
    apt clean

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# Debug only
RUN apt install vim procps -y --no-install-recommends && \
    apt clean

COPY ./pytask/ $APP_DIR/pytask
# not allowed
# COPY ./credentials/ $APP_DIR/credentials

RUN cd $APP_DIR && \
    pip3 install -r pytask/requirements.txt
    # python3 pytask/cron.py

COPY ./*.sh $APP_DIR/
COPY --from=builder ./go/src/server/server $APP_DIR/

EXPOSE $PORT
WORKDIR $APP_DIR

CMD ["sh", "./cron.sh"]