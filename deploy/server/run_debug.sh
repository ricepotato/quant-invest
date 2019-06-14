#!/bin/bash

docker run -it \
--name qi-server \
-p 8080:8080 \
--net=qinet \
qi-server:latest
