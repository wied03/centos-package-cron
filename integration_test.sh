#!/bin/sh

set -e
docker build -t wied03/$OS_int docker/$OS/integration

docker run -e \"OS=$OS\" -v `pwd`:/code -w /code -u nonrootuser -t wied03/$OS_int ./install_run.sh
