FROM centos:7.0.1406
RUN useradd -m nonrootuser -G wheel \
  && echo "nonrootuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN yum -y --disablerepo=updates swap -- remove fakesystemd -- install systemd systemd-libs \
yum clean all; \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*; \
yum -y --disablerepo=updates install rpm-build yum-utils sudo rpmlint postfix; \
yum clean all; \
sed -i 's/inet_protocols = all/inet_protocols = ipv4/' /etc/postfix/main.cf
CMD ["/bin/bash"]
