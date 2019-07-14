#!/bin/bash

docker run -it \
--rm \
--name qi-dev \
-p 8090:8090 \
-v /qi:/app/qi \
--net=qinet \
qi-dev:latest
