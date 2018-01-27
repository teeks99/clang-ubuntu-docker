FROM ubuntu:trusty
MAINTAINER Thomas Kent <teeks99@yahoo.com>

# Enable future toolchain PPA
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:ubuntu-toolchain-r/test

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
 zlib1g-dev \
 libstdc++-6-dev

RUN cd /usr/bin && ln -s python2.7 python

# Enable Repo
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 6084F3CF814B57C1CF12EFD515CF4D18AF4F7421
ADD llvm.list /etc/apt/sources.list.d/

# Install Tool
RUN apt-get update && apt-get install -y clang-3.7
