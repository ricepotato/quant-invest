#!/bin/bash
docker stop qi-web
docker rm qi-web
docker run -it \
--name qi-web \
--hostname=dockerhost-web \
--rm \
-e MODE=DEV \
-p 80:80 \
--net=qinet \
qi-web:latest
