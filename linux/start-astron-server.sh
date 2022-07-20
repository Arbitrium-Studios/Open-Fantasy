#!/bin/sh
cd ../astron/astron

# This assumes that your astrond build is located in the
# "astron/linux" directory.
./astrond --loglevel info ../config/astrond.yml
