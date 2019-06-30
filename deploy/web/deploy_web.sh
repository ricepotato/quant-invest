#!/bin/bash

cd ../../src/
tar -cvf web.tar ./web
gzip -v ./web.tar
tar -cvf common.tar ./common
gzip -v ./common.tar
mv web.tar.gz ../build/web/
mv common.tar.gz ../build/web/
cd ../build/web
./build.sh
