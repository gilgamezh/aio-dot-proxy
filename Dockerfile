FROM python:alpine
MAINTAINER Gilgamezh <mail@gilgamezh.me>

COPY . /usr/src/aio_dot_proxy 
WORKDIR /usr/src/aio_dot_proxy 
RUN python3 setup.py install

ENTRYPOINT ["/usr/local/bin/dot_proxy"]
