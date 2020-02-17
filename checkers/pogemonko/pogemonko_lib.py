from checklib import *
from pwn import *
context.log_level = "CRITICAL"
import requests

PORT = 9172


class CheckMachine:
    def __init__(self, checker):
        self.c = checker
        self.r = None

    def init_r(self):
        self.r = remote(self.c.host, PORT)

    def close_r(self):
        self.r.close()

    def register(self):
        username = rnd_username()
        password = rnd_password()
        self.r.recvuntil("> ")
        self.r.sendline("2")
        self.r.recvuntil("Input username: ")
        self.r.sendline(username)
        self.r.recvuntil("Input password: ")
        self.r.sendline(password)
        return username, password

    def login(self, username, password):
        self.r.recvuntil("> ")
        self.r.sendline("1")
        self.r.recvuntil("Input username: ")
        self.r.sendline(username)
        self.r.recvuntil("Input password: ")
        self.r.sendline(password)

    def logout(self):
        self.r.recvuntil("> ")
        self.r.sendline("4")

    def list_users(self):
        self.r.recvuntil("> ")
        self.r.sendline("3")
        s = self.r.recvuntil(b"Welcome").decode()[:-7].strip().split("\n")
        return s

    def catch_pokemon(self, desc, name):
        self.r.recvuntil("> ")
        self.r.sendline("1")
        self.r.recvuntil("Enter pokemon description: ")
        self.r.sendline(desc)
        self.r.recvuntil("Give it a name: ")
        self.r.sendline(name)

    def list_pokemons(self):
        self.r.recvuntil("> ")
        self.r.sendline("3")
        s = self.r.recvuntil(b"Welcome").decode()[:-7].strip()
        return s

    def fight_user(self, username):
        self.r.recvuntil("> ")
        self.r.sendline("2")
        self.r.recvuntil("Who do you want to fight: ")
        self.r.sendline(username)
        s = self.r.recvuntil(b"Welcome").decode()[:-7].strip()
        return s