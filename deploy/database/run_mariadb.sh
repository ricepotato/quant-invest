#!/bin/bash

docker run -d \
--name qidb \
--restart=always \
--net=qinet \
-p 3306:3306 \
-v /storage/qi/db:/var/lib/mysql \
-e MYSQL_DATABASE=qi \
-e MYSQL_USER=qi \
-e MYSQL_PASSWORD=password \
-e MYSQL_ROOT_PASSWORD=password \
mariadb:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
