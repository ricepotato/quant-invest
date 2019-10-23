#!/bin/sh
chown -R www.www /app

if [ $MODE == "DEV" ];
then
    /bin/sh
else
    ./start_server.sh
fi
