#!/bin/bash

docker run -it \
--name qi-web \
--rm \
-v /qi/src/web:/app/qi/web \
-v /var/log/django:/var/log/django \
-p 8090:8090 \
--net=qinet \
qi-web:latest
