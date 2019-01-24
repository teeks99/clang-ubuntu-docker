FROM ubuntu:bionic
MAINTAINER Thomas Kent <docker@teeks99.com>
ARG llvmver=9

ADD llvm.list /
ADD llvm-snapshot.gpg.key /

# Pre-Req Repos
RUN apt-get update \
 && apt-get install -y software-properties-common \
  gnupg \
# Install pre-reqs
 && mv llvm.list /etc/apt/sources.list.d/ \
 && apt-key add llvm-snapshot.gpg.key \
 && rm llvm-snapshot.gpg.key \
 && apt-get update \
 && apt-get install -y \
  ca-certificates \
  build-essential \
# Install Tool
  clang-$llvmver \
  clang-tools-$llvmver \
  clang-format-$llvmver \
  python-clang-$llvmver \
  libfuzzer-$llvmver-dev \
  lldb-$llvmver \
  lld-$llvmver \
  libc++-$llvmver-dev \
  libc++abi-$llvmver-dev \
  libomp-$llvmver-dev 

