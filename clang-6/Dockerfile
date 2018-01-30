FROM ubuntu:xenial
MAINTAINER Thomas Kent <docker@teeks99.com>

ADD llvm.list /etc/apt/sources.list.d/

# Pre-Req Repos
RUN apt-get update \
 && apt-get install -y software-properties-common \
 && add-apt-repository -y ppa:anthony-justsoftwaresolutions/libcxx \
# Enable Compiler Repo
 &&  apt-key adv --keyserver keyserver.ubuntu.com --recv 6084F3CF814B57C1CF12EFD515CF4D18AF4F7421 \
# Install pre-reqs
 && apt-get update \
 && apt-get install -y \
  ca-certificates \
  build-essential \

# Install Tool
  clang-6.0 \
  libc++-dev \
  libc++abi-dev

