#!/bin/bash
docker stop qi-web
docker rm qi-web
docker run -d \
--restart=always \
--name qi-web \
--hostname=dockerhost-web \
-p 80:80 \
--net=qinet \
qi-server:latest