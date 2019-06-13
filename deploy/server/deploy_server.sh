#!/bin/bash

cd ../../src/
tar -cvf server.tar ./server
gzip -v ./server.tar
mv server.tar.gz ../build/server/
cd ../build/server
./build.sh