#!/usr/bin/python

import unittest
import sys
import os
from centos_package_cron import mockable_execute

class MockableExecuteTestCase(unittest.TestCase):
    def testExecute(self):
        # arrange
        executor = mockable_execute.MockableExecute()

        # act
        result = executor.run_command(['cat','/etc/centos-release'])

        # assert
        expected_string = 'CentOS release 6.6 (Final)\n' if os.environ['CENTOS'] == 'centos6' else 'CentOS Linux release 7.0.1406 (Core) \n'
        self.assertEquals(result, expected_string)

if __name__ == "__main__":
            unittest.main()
