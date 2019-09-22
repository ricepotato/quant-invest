#!/bin/sh
chown -R www.www /app
nginx
uwsgi --ini web.ini

