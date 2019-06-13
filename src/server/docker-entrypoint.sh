#!/bin/bash

touch qi-server.log
chmod 755 ./*

uwsgi --http :8080 --master --callable app --wsgi-file server.py --processes 4 --logto ./qi-server.log