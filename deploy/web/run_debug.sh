#!/bin/bash

docker run -it \
--name qi-web \
-p 8090:8090 \
-v /qi:/app/qi \
--net=qinet \
qi-web:latest
