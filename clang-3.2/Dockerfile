FROM ubuntu:trusty
MAINTAINER Thomas Kent <teeks99@yahoo.com>

# Enable future toolchain PPA
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:h-rayflood/llvm

# Install pre-reqs
RUN apt-get update && apt-get install -y \
 ca-certificates \
 build-essential

# Install Tool
RUN apt-get update && apt-get install -y clang-3.2
