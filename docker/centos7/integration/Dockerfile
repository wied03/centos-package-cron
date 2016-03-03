FROM centos:7.0.1406
MAINTAINER Brady Wied <brady@bswtechconsulting.com>
RUN yum -y --disablerepo=updates swap -- remove fakesystemd -- install systemd systemd-libs
RUN yum clean all; \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
RUN useradd -m nonrootuser -G wheel
RUN echo "nonrootuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN yum -y --disablerepo=updates install rpm-build yum-utils sudo rpmlint
