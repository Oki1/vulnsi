#!/usr/bin/env python3

from pwn import *

exe = ELF("./main_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.43.so")

context.binary = exe


def conn():
    return gdb.debug(exe.path)


def main():
    r = conn()


    r.interactive()


if __name__ == "__main__":
    main()
