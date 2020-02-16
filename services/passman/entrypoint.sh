#!/bin/sh

set -e
cd /app

gunicorn --log-level info \
  --paste development.ini#main \
  --worker-class gevent \
  --worker-connections 1024 \
  -b 0.0.0.0:5000 \
  --capture-output
