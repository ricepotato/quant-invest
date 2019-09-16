#!/bin/sh

rc-service nginx start
uwsgi --ini server.ini
