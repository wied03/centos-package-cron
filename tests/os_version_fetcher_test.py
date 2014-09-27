#!/usr/bin/python

import unittest
import sys
sys.path.append('../lib')
import os_version_fetcher

class PackageCheckerTest(unittest.TestCase):
	def testget_complete_version(self):
		# arrange
		checker = os_version_fetcher.OsVersionFetcher()
		
		# act
		result = checker.get_complete_version()
		
		# assert
		self.assertEquals(result, '7.0.1406')
		
	def testget_top_level_version(self):
		# arrange
		checker = os_version_fetcher.OsVersionFetcher()

		# act
		result = checker.get_top_level_version()

		# assert
		self.assertEquals(result, '7')
		
if __name__ == "__main__":
            unittest.main()