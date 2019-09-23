#!/bin/bash
docker stop qi-server
docker rm qi-server
docker run -d \
--restart=always \
--name qi-server \
-p 8089:8089 \
--net=qinet \
qi-server:latest
