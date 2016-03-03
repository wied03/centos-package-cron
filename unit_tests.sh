#!/bin/bash

if [ "$CENTOS" == "centos67" ]
then
  # Don't have 6.7 compatible tests right now
  exit 0
fi

set -e
docker build -t wied03/${CENTOS}_unit docker/$CENTOS/unit

if [ "$CENTOS" == "centos7" ]
then
  OS=centos7
else
  OS=centos6
fi

# allow additional test args
docker run --rm=true -e "CENTOS=${OS}" -v `pwd`:/code -w /code -u nonrootuser -t wied03/${CENTOS}_unit ./setup.py test $*
