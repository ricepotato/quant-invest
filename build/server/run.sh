#!/bin/bash

docker run -it \
--name qi-server \
-p 8089:80 \
--net=qinet \
qi-server:latest
