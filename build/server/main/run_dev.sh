#!/bin/bash
docker stop qi-server
docker rm qi-server
docker run -it \
--name qi-server \
-p 8089:80 \
-p 8091:8091 \
-e MODE=DEV \
--net=qinet \
qi-server:latest
