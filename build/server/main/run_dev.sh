#!/bin/bash
docker stop qi-server
docker rm qi-server
docker run -it \
--name qi-server \
-p 8089:8089 \
-e MODE=DEV \
--net=qinet \
qi-server:latest
