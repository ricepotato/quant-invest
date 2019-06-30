#!/bin/bash

docker run -d \
--name qi-server \
-p 8090:8090 \
--net=qinet \
qi-server:latest