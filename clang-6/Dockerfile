FROM ubuntu:xenial
MAINTAINER Thomas Kent <docker@teeks99.com>

# Pre-Req Repos
RUN apt-get update \
 && apt-get install -y software-properties-common \
 && add-apt-repository -y ppa:git-core/ppa \
 && add-apt-repository -y ppa:anthony-justsoftwaresolutions/libcxx \
# Install pre-reqs
 && apt-get update \
 && apt-get install -y \
  ca-certificates \
  build-essential \
  git \
  wget \
  python2.7 \
  python2.7-dev \
  python3.5 \
  python3.5-dev \
  libbz2-dev \
  zlib1g-dev \
 && cd /usr/bin \
 && ln -s python2.7 python \
# Speed up fetch
 && git config --global submodule.fetchJobs 40

# Enable Compiler Repo
ADD llvm.list /etc/apt/sources.list.d/
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 6084F3CF814B57C1CF12EFD515CF4D18AF4F7421 \
# Install Tool
 && apt-get update \
 && apt-get install -y clang-6.0 libc++-dev libc++abi-dev

