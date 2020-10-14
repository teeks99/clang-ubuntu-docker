FROM ubuntu:xenial
MAINTAINER Thomas Kent <docker@teeks99.com>

# Pre-Req Repos
RUN apt-get update \
 && apt-get install -y \
  software-properties-common \
# Needed for repo access
  apt-transport-https \
  ca-certificates

ADD llvm.list /etc/apt/sources.list.d/

RUN add-apt-repository -y ppa:anthony-justsoftwaresolutions/libcxx \
# Enable Compiler Repo
 &&  apt-key adv --keyserver keyserver.ubuntu.com --recv 6084F3CF814B57C1CF12EFD515CF4D18AF4F7421 \
# Install pre-reqs
 && apt-get update \
 && apt-get install -y \
  build-essential \
# Install Tool
  clang-6.0 \
  libc++-dev \
  libc++abi-dev

