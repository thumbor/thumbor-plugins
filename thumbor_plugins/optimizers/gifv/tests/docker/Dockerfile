FROM python:3.9-slim

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y \
        gifsicle \
        ffmpeg &&\
    apt-get clean
