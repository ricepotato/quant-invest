#!/bin/bash

cd ../../src/
tar -cvf server.tar ./server
gzip -v ./server.tar
tar -cvf common.tar ./common
gzip -v ./common.tar
mv server.tar.gz ../build/server/
mv common.tar.gz ../build/server/
cd ../build/server
./build.sh