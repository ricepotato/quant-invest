#!/bin/bash

docker run -d \
--name qi-server \
-p 8080:8080 \
--net=qinet \
qi-server:latest
