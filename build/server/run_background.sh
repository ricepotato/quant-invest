#!/bin/bash
docker stop qi-server
docker rm qi-server
docker run -d \
--restart=always \
--name qi-server \
-p 8089:80 \
--net=qinet \
qi-server:latest
