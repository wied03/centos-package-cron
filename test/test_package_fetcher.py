#!/usr/bin/python

import unittest
import sys
sys.path.append('../lib')
import package_fetcher
from mock import Mock

class ChangeLogParserTestCase(unittest.TestCase):
	def testParse(self):
		# arrange
		parser = package_fetcher.ChangeLogParser()
		output = open('changelog_raw_output.txt').read()
		
		# act
		results = parser.parse(output,'bash','4.2.45','5.el7_0.4')
		
		# assert
		expected_output = """* Thu Sep 25 07:00:00 2014 Ondrej Oprala <ooprala@redhat.com> - 4.2.45-5.4
- CVE-2014-7169
  Resolves: #1146324

"""
		self.assertEquals(results,expected_output)
		
	def testNotFound(self):
		# arrange
		parser = package_fetcher.ChangeLogParser()
		output = open('changelog_raw_output.txt').read()
		
		# act
		try:
			parser.parse(output,'bash','4.4','5.el7_0.4')
		except:
			if sys.exc_info()[0] == 'Unable to find this':
				pass
			else:
				raise
		else:
			fail("Expected exception")		

class PackageFetcherTestCase(unittest.TestCase):
	def testfetch_installed_packages(self):
		# arrange
		ch_log_parser = Mock()
		fetcher = package_fetcher.PackageFetcher(ch_log_parser)
		
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
		
	def testFetch_package_updates(self):
		# arrange
		ch_log_parser = Mock()
		fetcher = package_fetcher.PackageFetcher(ch_log_parser)
		
		# act
		result = fetcher.get_package_updates()
		
		# assert
		self.assertGreater(len(result),0)
		first_package = result[0]
		assert isinstance(first_package, package_fetcher.Package)
		print "1st package name is %s" % (first_package.name)
		self.assertNotEquals(first_package.name, None)
		print "1st package version is %s" % (first_package.version)
		self.assertNotEquals(first_package.version, None)
		print "1st package release is %s" % (first_package.release)
		self.assertNotEquals(first_package.release, None)
		self.assertNotEquals(first_package.arch, None)
		
	def testGetPackageChangeLog(self):
		# arrange
		
		# act
		
		# assert
		raise 'write test'
		
if __name__ == "__main__":
            unittest.main()