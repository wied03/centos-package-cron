#!/bin/bash

set -e
docker build -t wied03/${CENTOS}_int docker/$CENTOS/integration

ZIP_FILE=centos_package_cron_src.tgz
rm -f $ZIP_FILE
# clean build
git archive -o $ZIP_FILE HEAD

docker run --rm=true -v `pwd`:/code -w /code -u nonrootuser -t wied03/${CENTOS}_int /code/install_and_run.sh $ZIP_FILE
