ARG release=jammy
ARG distro=ubuntu
FROM $distro:$release
MAINTAINER Thomas Kent <docker@teeks99.com>
ARG llvmver=17

# Pre-Req Repos
RUN apt-get update \
 && apt-get install -y \
  software-properties-common \
  gnupg \
# Needed for repo access
  apt-transport-https \
  ca-certificates 

ADD llvm.list /etc/apt/sources.list.d/
ADD llvm-snapshot.gpg.key.gpg /etc/apt/trusted.gpg.d/

# Install pre-reqs
RUN apt-get update \
 && apt-get install -y \
  ca-certificates \
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
  libomp-$llvmver-dev 

