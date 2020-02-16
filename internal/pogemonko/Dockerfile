FROM ubuntu:16.04

RUN apt update && \
    apt install -y gcc make

RUN mkdir -p /var/pogemonko/
RUN mkdir -p /var/build/

WORKDIR /var/pogemonko/

ADD . ./

RUN make

RUN chmod +x pogemonko

CMD ["mv", "pogemonko", "/var/build/"]