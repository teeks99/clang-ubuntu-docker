FROM ubuntu:trusty
MAINTAINER Thomas Kent <teeks99@yahoo.com>

# Enable future toolchain PPA
RUN apt-get update \
 && apt-get install -y software-properties-common \
# Install pre-reqs
 && apt-get update \
 && apt-get install -y \
  build-essential \
# Install Tool
  clang-3.4 \
# Make a versiond symlink                                                                                           │·
 && cd /usr/bin \
 && ln -s clang++ clang++-3.4
