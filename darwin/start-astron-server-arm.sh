#!/bin/sh
cd ../astron/darwin

# This assumes that your astrond build is located in the
# "astron/darwin" directory.
./astrond-arm --loglevel info ../config/astrond.yml
