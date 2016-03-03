FROM centos:6.7
MAINTAINER Brady Wied <brady@bswtechconsulting.com>
RUN yum -y --disablerepo=updates install python-setuptools git epel-release yum-utils
RUN yum -y --disablerepo=updates install python-pip mailx python-sqlalchemy sudo
# Newer versions of mock need setuptools > 17.0
RUN pip install setuptools --upgrade
# UID 1000 is what current (Mac/boot2docker) code directory shows up as being owned by
RUN useradd -m nonrootuser -G wheel -u 1000
RUN echo "nonrootuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
# is a disabled repo by default that also doesn't seem to exist anymore
RUN rm /etc/yum.repos.d/CentOS-Media.repo; yum clean all
