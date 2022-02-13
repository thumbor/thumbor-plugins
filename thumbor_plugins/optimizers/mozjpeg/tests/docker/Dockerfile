FROM python:3.9-slim

WORKDIR /app
RUN apt-get update -y && \
    apt-get install -y \
        wget \
        cmake \
        autoconf \
        automake \
        libtool \
        nasm \
        make \
        pkg-config \
        zlib1g-dev \
        libpng-dev && \
    wget https://github.com/mozilla/mozjpeg/archive/refs/tags/v4.0.3.tar.gz && \
    tar xf v4.0.3.tar.gz && \
    cd mozjpeg-4.0.3/ && \
    mkdir build && \
    cd build && \
    cmake -G"Unix Makefiles" ../ && \
    make install && \
    cd /app && \
    rm -rf v4.0.3.tar.gz mozjpeg-4.0.3 && \
    apt-get purge -y \
        wget \
        cmake \
        autoconf \
        automake \
        libtool \
        nasm \
        make \
        pkg-config && \
    apt-get clean && \
    /opt/mozjpeg/bin/cjpeg -version

