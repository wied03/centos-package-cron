#!/usr/bin/python

import unittest
import sys
sys.path.append('../lib')
import package_fetcher

class PackageFetcherTestCase(unittest.TestCase):
	def testfetch_installed_packages(self):
		# arrange
		fetcher = package_fetcher.PackageFetcher()
		
		# act
		result = fetcher.fetch_installed_packages()
		
		# assert
		assert len(result) >= 271, "Actual size is %d" % (len(result))
		first_package = result[0]
		assert isinstance(first_package, package_fetcher.Package)
		print "1st package name is %s" % (first_package.name)
		assert first_package.name != None
		print "1st package version is %s" % (first_package.version)
		assert first_package.version != None
		print "1st package release is %s" % (first_package.release)
		assert first_package.release != None
		self.assertEquals(first_package.arch, 'x86_64')		
		
if __name__ == "__main__":
            unittest.main()