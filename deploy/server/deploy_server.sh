#!/bin/bash

tar -cvf ../../server.tar ../../server
gzip -v ../../server.tar
mv ../../server.tar.gz ../../build/server
#../../build/server/build.sh