FROM ubuntu:20.04

EXPOSE 1337

RUN export DEBIAN_FRONTEND=noninteractive && \
    dpkg --add-architecture i386 && \
    apt-get -y update && \
    apt-get -y install socat coreutils libc6:i386 libstdc++6:i386 gdbserver binutils

COPY flag.txt /
COPY app /
COPY entrypoint.sh /

RUN chmod 555 /entrypoint.sh && \
    chmod 555 /app && \
    chmod 444 /flag.txt

CMD ["/entrypoint.sh"]
