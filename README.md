# Centos-Package-Cron

Attempts to offer Apticron (Ubuntu) style package update emails and also bring security notifications to CentOS via Meier's script

## What does it do?

* Checks for updates using Yum's Python API and changelogs for those updates using Yum's changelog plugin
* Checks security errata from CentOS mailing list via [Steve Meier's list](http://cefs.steve-meier.de/errata.latest.xml) and picks only advisories related to packages installed on your machine
* Emails the above information to an address of your choosing

## Installation

### Using Python

```shell
sudo yum install mailx yum-plugin-changelog
./setup.py install
```

### Using RPM

```shell
rpmbuild -bb --verbose -D "_topdir `pwd`" -D "_sourcedir `pwd`" -D "_builddir `pwd`" centos-package-cron.spec
sudo yum install centos-package-cron-1.0.2-0.1.el7.centos.x86_64.rpm
```

## Usage

```shell
centos-package-cron --email-to sysadmin@stuff.com --email_from dev@somebox.com
# See centos-package-cron -h for options
```

## TODO
* Add ability to not be reminded about updates more than once