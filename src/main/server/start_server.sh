#!/bin/sh
chown -R www.www /app
nginx
uwsgi --ini server.ini
