FROM ubuntu:trusty
MAINTAINER Thomas Kent <teeks99@yahoo.com>

# Enable future toolchain PPA
RUN apt-get update && apt-get install -y software-properties-common 

# Install pre-reqs
RUN apt-get update && apt-get install -y \
 build-essential
 
# Install Tool
RUN apt-get update && apt-get install -y clang-3.3
# Make a versiond symlink
RUN cd /usr/bin && ln -s clang++ clang++-3.3
