#!/bin/bash

docker network rm qinet
docker network create --driver=bridge \
--subnet=172.25.0.0/16 \
--ip-range=172.25.0.0/24 \
--gateway=172.25.0.1 \
qinet
docker network inspect qinet
