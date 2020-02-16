FROM ubuntu:16.04

MAINTAINER tg: @kekov

RUN apt update && \
    apt install -y socat

RUN mkdir -p /var/pogemonko/

WORKDIR /var/pogemonko/

ADD pogemonko ./

CMD ["socat", "TCP-LISTEN:31337,reuseaddr,fork", "EXEC:./pogemonko"]