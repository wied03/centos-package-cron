#!/usr/bin/python

import unittest
import sys
from centos_package_cron import mockable_execute

class MockableExecuteTestCase(unittest.TestCase):
	def testExecute(self):
		# arrange
		executor = mockable_execute.MockableExecute()
		
		# act
		result = executor.run_command(['cat','/etc/centos-release'])
		
		# assert
		self.assertEquals(result, 'CentOS Linux release 7.0.1406 (Core) \n')
		
if __name__ == "__main__":
            unittest.main()
