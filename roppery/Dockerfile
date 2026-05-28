FROM ubuntu:20.04@sha256:e5a6aeef391a8a9bdaee3de6b28f393837c479d8217324a2340b64e45a81e0ef

EXPOSE 1337

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install gcc socat coreutils

COPY chall/app.c /app.c
COPY chall/flag.txt /flag.txt

RUN gcc -fno-stack-protector -no-pie -o /app /app.c

RUN chmod 555 /app && \
    chmod 444 /flag.txt

CMD socat -T 30 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 /app"
