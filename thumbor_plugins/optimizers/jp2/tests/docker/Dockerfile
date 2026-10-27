FROM python:3.10-slim

WORKDIR /app
RUN apt-get update -y && \
    apt-get install -y \
        libopenjp2-7 \
        libopenjp2-7-dev && \
    apt-get clean

