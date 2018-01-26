FROM centos:7.0.1406
RUN useradd -m nonrootuser -G wheel \
  && echo "nonrootuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
  && yum -y --disablerepo=updates install sudo \
  && yum clean all \
  && rm -rf /tmp/*
CMD ["/bin/bash"]
