#!/bin/bash

set -e
mkdir /tmp/rpm
cd /code
rpmlint centos-package-cron.spec
sudo yum-builddep -y --disablerepo=updates centos-package-cron.spec
rpmbuild -ba --verbose -D "_topdir /tmp/rpm" -D "_sourcedir /tmp/rpm" -D "_builddir /tmp/rpm" centos-package-cron.spec
sudo yum -y --disablerepo=updates install RPMS/x86_64/*.rpm

# Now should be installed, let's try running
sudo mkdir -p /var/lib/centos-package-cron
sudo chown nonrootuser /var/lib/centos-package-cron
centos-package-cron --output stdout
