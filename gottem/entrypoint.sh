#!/bin/bash
socat -T 30 TCP-LISTEN:5000,nodelay,reuseaddr,fork EXEC:'stdbuf -i0 -o0 -e0 /app/main' &
socat -T 300 TCP-LISTEN:5050,nodelay,reuseaddr,fork EXEC:'stdbuf -i0 -o0 -e0 gdbserver \:9090 /app/main' &
wait
