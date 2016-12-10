FROM centos:7.0.1406
MAINTAINER Brady Wied <brady@bswtechconsulting.com>
RUN useradd -m nonrootuser -G wheel
RUN echo "nonrootuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN yum -y --disablerepo=updates install rpm-build yum-utils sudo rpmlint
