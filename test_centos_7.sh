#!/bin/sh

set -e
docker build -t wied03/centos_cron_7 docker/centos_cron_7
COMMAND="./setup.py test"
if [ -n "$*" ]
then
	ESCAPED=`echo $(printf '%q' $*)`
	COMMAND="$COMMAND -a $ESCAPED"
fi
echo "Running using $COMMAND"
# Using host networking for performance
docker run --rm -v `pwd`:/code -w /code --net=host -u nonrootuser -t wied03/centos_cron_7 $COMMAND
