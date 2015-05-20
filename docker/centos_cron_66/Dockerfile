FROM centos:6.6
MAINTAINER Brady Wied <brady@bswtechconsulting.com>
RUN yum -y --disablerepo=updates install python-setuptools git epel-release yum-utils
RUN yum -y --disablerepo=updates install python-pip mailx python-sqlalchemy sudo
# UID 1000 is what current (Mac/boot2docker) code directory shows up as being owned by
RUN useradd -m nonrootuser -G wheel -u 1000
RUN echo "nonrootuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
