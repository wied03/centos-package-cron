#!/bin/bash

set -e
docker build -t wied03/${CENTOS}_unit docker/$CENTOS/unit

# allow additional test args
docker run --rm=true -e "CENTOS=${CENTOS}" -v `pwd`:/code -w /code -u nonrootuser -t wied03/${CENTOS}_unit ./setup.py test $*
