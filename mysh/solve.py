from pwn import *
host_binary_path = "app"
subprocess.run(["docker", "exec", "-u", "root", "debug_container", "bash", "-c", "pkill -9 gdbserver || true"])
p = remote("127.0.0.1", 5050)   # connecting here spawns /app frozen under gdbserver
#p = remote("inst-hwykydorn8.tls.vuln.si", 443, ssl=True)   # connecting here spawns /app frozen under gdbserver
gdb.attach(('127.0.0.1', 9090), exe=host_binary_path, gdbscript='b main')


p.interactive()
