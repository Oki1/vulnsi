#!/usr/local/bin/python

import string
import tempfile
import os

allowed = string.ascii_letters + string.digits + "+-=()"

print("Send me your code, I will comment it properly and run it for you: ")

temp = tempfile.NamedTemporaryFile()

while (line := input().strip()):
    if any(c not in allowed for c in line):
        print("Invalid character detected")
        exit(1)
    temp.write((f"#{line}\n").encode())

temp.flush()

print(temp.name)
os.system(f"python3 {temp.name}")
# input()
