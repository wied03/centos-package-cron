#!/usr/bin/env python

import setuptools

setuptools.setup(name='centos_package_cron',
      version='1.0',
      description='CentOS Package Update Utilities',
      author='Brady Wied',
      author_email='support@bswtechconsulting.com',
      url='https://github.com/wied03/centos-package-cron',
      packages=setuptools.find_packages(),
      test_suite="tests",
      tests_require="mock"
     )
