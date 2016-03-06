#!/bin/bash

set -e
set -x

sudo yum -y --disablerepo=updates install /code/built_rpms/RPMS/x86_64/*.rpm

# Now should be installed, let's try running
sudo mkdir -p /var/lib/centos-package-cron
sudo chown nonrootuser /var/lib/centos-package-cron
# see version info, etc. in help
centos-package-cron --help
centos-package-cron --output stdout
