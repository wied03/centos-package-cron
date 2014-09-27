#!/usr/bin/env python

from distutils.core import setup
from setuptools import setup, find_packages	

setup(name='centos_package_cron',
      version='1.0',
      description='CentOS Package Update Utilities',
      author='Brady Wied',
      author_email='support@bswtechconsulting.com',
      url='https://github.com/wied03/centos-package-cron',
      packages=find_packages(),
      test_suite="tests"
     )
