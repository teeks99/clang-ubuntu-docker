FROM ubuntu:trusty
MAINTAINER Thomas Kent <teeks99@yahoo.com>

ADD llvm.list /etc/apt/sources.list.d/

# Enable future toolchain PPA
RUN apt-get update \
 && apt-get install -y software-properties-common \
 && add-apt-repository -y ppa:ubuntu-toolchain-r/test \
# Enable Compiler Repo
 &&  apt-key adv --keyserver keyserver.ubuntu.com --recv 6084F3CF814B57C1CF12EFD515CF4D18AF4F7421 \
# Install pre-reqs
 && apt-get update \
 && apt-get install -y \
  build-essential \
  libstdc++-6-dev \

# Install Tool
  clang-3.5
