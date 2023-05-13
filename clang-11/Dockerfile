ARG release=focal
ARG distro=ubuntu
FROM $distro:$release
MAINTAINER Thomas Kent <docker@teeks99.com>
ARG llvmver=11

# Pre-Req Repos
RUN apt-get update \
 && apt-get install -y \
  software-properties-common \
  gnupg \
# Needed for repo access
  apt-transport-https \
  ca-certificates

ADD llvm.list /
ADD llvm-snapshot.gpg.key /

# Install pre-reqs
RUN mv llvm.list /etc/apt/sources.list.d/ \
 && apt-key add llvm-snapshot.gpg.key \
 && rm llvm-snapshot.gpg.key \
 && apt-get update \
 && apt-get install -y \
  build-essential \
# Install Tool
  clang-$llvmver \
  clang-tools-$llvmver \
  clang-format-$llvmver \
  python3-clang-$llvmver \
  libfuzzer-$llvmver-dev \
  lldb-$llvmver \
  lld-$llvmver \
  libc++-$llvmver-dev \
  libc++abi-$llvmver-dev \
  libomp-$llvmver-dev \
 # Make an alias for the versioned executable
 && ln -s /usr/bin/clang++-$llvmver /usr/bin/clang++
