#!/bin/bash

set -e
cd /tmp
mkdir rpm
cd rpm
unzip /code/$1
rpmlint centos-package-cron.spec
sudo yum-builddep -y --disablerepo=updates centos-package-cron.spec
rpmbuild -bb --verbose -D "_topdir `pwd`" -D "_sourcedir `pwd`" -D "_builddir `pwd`" centos-package-cron.spec
sudo yum -y --disablerepo=updates install RPMS/x86_64/*.rpm

# Now should be installed, let's try running
sudo mkdir -p /var/lib/centos-package-cron
sudo chown nonrootuser /var/lib/centos-package-cron
centos-package-cron --output stdout
