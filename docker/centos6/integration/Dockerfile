FROM centos:6.6
MAINTAINER Brady Wied <brady@bswtechconsulting.com>
RUN useradd -m nonrootuser -G wheel
RUN echo "nonrootuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN yum -y --disablerepo=updates install rpm-build yum-utils sudo rpmlint tar
# is a disabled repo by default that also doesn't seem to exist anymore
RUN rm /etc/yum.repos.d/CentOS-Media.repo; yum clean all
