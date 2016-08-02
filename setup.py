#!/usr/bin/env python

import sys
import setuptools

from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setuptools.setup(name='centos_package_cron',
      version='1.0.8.1',
      description='CentOS Package Update Utilities',
      author='Brady Wied',
      author_email='support@bswtechconsulting.com',
      url='https://github.com/wied03/centos-package-cron',
      packages=setuptools.find_packages(),
      setup_requires="pytest",
      tests_require="mock",
      cmdclass = {'test': PyTest},
	  entry_points = {
	        'console_scripts': ['centos-package-cron=centos_package_cron.command_line:main'],
	  }
     )
