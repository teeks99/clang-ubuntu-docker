ARG release=noble
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
  apt-transport-https

ADD llvm.list /etc/apt/sources.list.d/
ADD llvm-snapshot.gpg.key.gpg /etc/apt/trusted.gpg.d/

# Install pre-reqs
RUN apt-get update \
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
  libunwind-$llvmver-dev \
  libpolly-$llvmver-dev \
  libclc-$llvmver-dev \
  # MLIR
  libmlir-15-dev mlir-15-tools \
  # Bolt
  # Doesn't work on aarch64 libbolt-$llvmver-dev bolt-$llvmver \
  # LLVM WASM
  libclang-rt-$llvmver-dev-wasm32 \
  libclang-rt-$llvmver-dev-wasm64 \
  libc++-$llvmver-dev-wasm32 \
  libc++abi-$llvmver-dev-wasm32 \
  libclang-rt-$llvmver-dev-wasm32 \
  libclang-rt-$llvmver-dev-wasm64 \
 # Make an alias for the versioned executable
 && ln -s /usr/bin/clang++-$llvmver /usr/bin/clang++ \
 && ln -s /usr/bin/clang-$llvmver /usr/bin/clang
 