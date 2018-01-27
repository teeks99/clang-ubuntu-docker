FROM ubuntu:trusty
MAINTAINER Thomas Kent <teeks99@yahoo.com>

# Enable future toolchain PPA
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:h-rayflood/llvm

# Install pre-reqs
RUN apt-get update && apt-get install -y \
 ca-certificates \
 build-essential \
 git \
 wget \
 python2.7 \
 python2.7-dev \
 python3.4 \
 python3.4-dev \
 libbz2-dev \
 zlib1g-dev
RUN cd /usr/bin && ln -s python2.7 python

# Install Tool
RUN apt-get update && apt-get install -y clang-3.1
