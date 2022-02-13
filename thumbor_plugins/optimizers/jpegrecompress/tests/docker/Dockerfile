FROM python:3.9-slim

WORKDIR /app

RUN wget https://github.com/danielgtaylor/jpeg-archive/releases/download/2.1.1/jpeg-archive-2.1.1-linux.tar.bz2 && \
    tar -zxvf https://github.com/danielgtaylor/jpeg-archive/releases/download/2.1.1/jpeg-archive-2.1.1-linux.tar.bz2 && \
    mv jpeg-recompress /usr/bin/ && \
    rm https://github.com/danielgtaylor/jpeg-archive/releases/download/2.1.1/jpeg-archive-2.1.1-linux.tar.bz2
