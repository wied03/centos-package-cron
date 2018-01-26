FROM wied03/centos_cron/centos7/run:latest
MAINTAINER Brady Wied <brady@bswtechconsulting.com>
RUN yum -y --disablerepo=updates install python-setuptools git epel-release yum-utils; yum clean all \
  && yum -y --disablerepo=updates install python-pip mailx python-sqlalchemy rpm-build rpmlint; yum clean all \
  # Newer versions of mock need setuptools > 17.0
  && pip install --upgrade pip && pip install setuptools --upgrade \
  && rm -rf /tmp/*
