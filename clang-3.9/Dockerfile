FROM ubuntu:xenial
MAINTAINER Thomas Kent <docker@teeks99.com>

# Pre-Req Repos
RUN apt-get update && apt-get install -y software-properties-common

# Install pre-reqs
RUN apt-get update && apt-get install -y \
 ca-certificates \
 build-essential

# Enable Compiler Repo
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 6084F3CF814B57C1CF12EFD515CF4D18AF4F7421
ADD llvm.list /etc/apt/sources.list.d/

# Install Tool
RUN apt-get update && apt-get install -y clang-3.9 libc++-dev libc++abi-dev

