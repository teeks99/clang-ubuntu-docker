FROM ubuntu:xenial
MAINTAINER Thomas Kent <docker@teeks99.com>

# Pre-Req Repos
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:git-core/ppa

# Install pre-reqs
RUN apt-get update && apt-get install -y \
 ca-certificates \
 build-essential \
 git \
 wget \
 python2.7 \
 python2.7-dev \
 python3.5 \
 python3.5-dev \
 libbz2-dev \
 zlib1g-dev
RUN cd /usr/bin && ln -s python2.7 python

# Enable Compiler Repo
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 6084F3CF814B57C1CF12EFD515CF4D18AF4F7421
#ADD llvm.list /etc/apt/sources.list.d/

# Install Tool
#RUN apt-get update && apt-get install -y clang-4.0 libc++-dev libc++abi-dev
RUN cd /home \
 && wget http://releases.llvm.org/4.0.0/clang+llvm-4.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz \
 && tar -xf clang+llvm-4.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz \
 && ln -s /home/clang+llvm-4.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang-4.0 /usr/bin/clang++-4.0 \
 && cp -r /home/clang+llvm-4.0.0-x86_64-linux-gnu-ubuntu-16.04/lib/*.a /usr/lib/ \
 && cp -r /home/clang+llvm-4.0.0-x86_64-linux-gnu-ubuntu-16.04/lib/*.so* /usr/lib/ \
 && cp -r /home/clang+llvm-4.0.0-x86_64-linux-gnu-ubuntu-16.04/include/* /usr/include/ 

# Symlink tools


# Add the tool configs
ADD user-config.jam /

# Fix a ubuntu bug
ADD fix_string.py /
RUN python fix_string.py 

