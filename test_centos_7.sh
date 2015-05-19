#!/bin/sh

docker build -t wied03/centos_cron_7 docker/centos_cron_7
docker run --rm -v `pwd`:/code -w /code wied03/centos_cron_7 ./setup.py test
