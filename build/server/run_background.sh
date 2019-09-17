#!/bin/bash

docker run -d \
--restart=always \
--name qi-server \
-p 8089:80 \
--net=qinet \
qi-server:latest
