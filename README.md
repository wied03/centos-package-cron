# Centos-Package-Cron

[![Build Status](http://img.shields.io/travis/wied03/centos-package-cron/master.svg?style=flat)](http://travis-ci.org/wied03/centos-package-cron)
[![Quality](http://img.shields.io/codeclimate/github/wied03/centos-package-cron.svg?style=flat-square)](https://codeclimate.com/github/wied03/centos-package-cron)

Attempts to offer Apticron (Ubuntu) style package update emails and also bring security notifications to CentOS via Meier's script

## What does it do?

* Checks for updates using Yum's Python API and changelogs for those updates using Yum's changelog plugin
* Checks security errata from CentOS mailing list via [Steve Meier's list](http://cefs.steve-meier.de/errata.latest.xml) and picks only advisories related to packages installed on your machine
* Emails the above information to an address of your choosing
* By default, only reminds about a given security advisory / package update once to avoid annoying you.  You can change this using the --skipold false option (see -h)

## Requirements

* Tested on CentOS 7 and 6.6, but coded in a way that should work even CentOS 5. The dependencies as listed in the RPM spec might need to be tweaked to run properly on CentOS < 7. If you can help test with that, feel free to create a pull request.

## Installation

### Using Python

```shell
sudo yum install mailx yum-plugin-changelog
./setup.py install
# For the SQLite DB that avoids reminding you of updates that were already sent (see above)
mkdir /var/lib/centos-package-cron
```

### Using RPM

*CentOS package submission pending*

If you use Docker, you can checkout this repository and build an RPM this way:

```shell
# use centos6 if that applies
CENTOS=centos7 ./build_package.sh
```

If you'd rather not use Docker, then do something like this:
```shell
sudo yum install rpm-build yum-utils
sudo yum-builddep -y --disablerepo=updates centos-package-cron.spec
# Download a tar gzip of the source to /some/path/containing/source/centos_package_cron_src.tgz
rpmbuild -bb --verbose -D "_topdir `pwd`" -D "_sourcedir /some/path/containing/source" -D "_builddir `pwd`" centos-package-cron.spec
sudo yum install centos-package-cron-1.0.6-0.1.el7.centos.x86_64.rpm
```

## Usage

```shell
centos-package-cron --email_to sysadmin@stuff.com --email_from dev@somebox.com
# See centos-package-cron -h for options
```
