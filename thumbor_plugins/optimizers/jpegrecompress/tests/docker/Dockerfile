FROM python:3.9-slim

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y wget bzip2 && \
    wget https://github.com/danielgtaylor/jpeg-archive/releases/download/2.1.1/jpeg-archive-2.1.1-linux.tar.bz2 && \
    tar -jxvf jpeg-archive-2.1.1-linux.tar.bz2 && \
    mv jpeg-recompress /usr/bin/ && \
    rm jpeg-archive-2.1.1-linux.tar.bz2 && \
    apt-get purge -y wget bzip2 && \
    apt-get clean
