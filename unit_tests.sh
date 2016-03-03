#!/bin/sh

set -e
docker build -t wied03/$OS_unit docker/$OS/unit

# allow additional test args
docker run -e \"OS=$OS\" -v `pwd`:/code -w /code -u nonrootuser -t wied03/$OS_unit ./setup.py test $*
