FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
RUN tar -xf Python-3.7.2.tar.xz
WORKDIR /tmp/Python-3.7.2
RUN ./configure --enable-optimizations
RUN make -j 1
RUN make altinstall
RUN rm -rf /tmp/Python-3.7.2
RUN rm -rf /tmp/Python-3.7.2.tar.xz
RUN ln -s /usr/local/bin/python3.7 /usr/local/bin/python
RUN ln -s /usr/local/bin/pip3.7 /usr/local/bin/pip
WORKDIR /root