FROM ubuntu:bionic
MAINTAINER Thomas Kent <docker@teeks99.com>

ADD llvm.list /etc/apt/sources.list.d/
ADD llvm-snapshot.gpg.key /

# Pre-Req Repos
RUN apt-key add llvm-snapshot.gpg.key \
 && apt-get update \
 && apt-get install -y software-properties-common \
# Install pre-reqs
 && apt-get update \
 && apt-get install -y \
  ca-certificates \
  build-essential \

# Install Tool
  clang-7 \
  clang-tools-7 \
  clang-format-7 \
  python-clang-7 \
  libfuzzer-7-dev \
  lldb-7 \
  lld-7 \
  libc++-7-dev \
  libc++abi-7-dev \
  libomp-7-dev 

