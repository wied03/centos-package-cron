#!/usr/bin/python
# coding: latin-1

import unittest
import sys
from centos_package_cron import package_fetcher
from mock import Mock
from centos_package_cron import mockable_execute

class ChangeLogParserTestCase(unittest.TestCase):
	def testGet_log_version_num_suffix(self):
		# arrange
		parser = package_fetcher.ChangeLogParser()
		
		# act
		result = parser.get_log_version_num('1.0.1e','34.el7_0.4')
		
		# assert
		self.assertEquals(result,'1.0.1e-34.4')
	
	def testGet_log_version_num_no_suffix(self):
		# arrange
		parser = package_fetcher.ChangeLogParser()
		
		# act
		result = parser.get_log_version_num('2014.1.98','70.0.el7_0')
		
		# assert
		self.assertEquals(result,'2014.1.98-70.0')
	
	def testGet_log_version_num_rhel_7(self):
		# arrange
		parser = package_fetcher.ChangeLogParser()
		
		# act
		result = parser.get_log_version_num('4.2.45','5.el7_0.4')
		
		# assert
		self.assertEquals(result,'4.2.45-5.4')	
		
	def testParseStandardRhel(self):
		# arrange
		parser = package_fetcher.ChangeLogParser()
		output = open('tests/complete_log.txt').read()
		
		# act
		results = parser.parse(output,'bash','4.2.45','5.el7_0.4')
		
		# assert
		expected_output = """* Thu Sep 25 07:00:00 2014 Ondrej Oprala <ooprala@redhat.com> - 4.2.45-5.4
- CVE-2014-7169
  Resolves: #1146324

"""
		self.assertEquals(results,expected_output)
		
	def testParseCentos(self):
		# arrange
		parser = package_fetcher.ChangeLogParser()
		output = open('tests/complete_log.txt').read()

		# act
		results = parser.parse(output,'openssl','1.0.1e','34.el7_0.4')

		# assert
		expected_output = """* Fri Aug  8 07:00:00 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-34.4
- fix CVE-2014-3505 - doublefree in DTLS packet processing
- fix CVE-2014-3506 - avoid memory exhaustion in DTLS
- fix CVE-2014-3507 - avoid memory leak in DTLS
- fix CVE-2014-3508 - fix OID handling to avoid information leak
- fix CVE-2014-3509 - fix race condition when parsing server hello
- fix CVE-2014-3510 - fix DoS in anonymous (EC)DH handling in DTLS
- fix CVE-2014-3511 - disallow protocol downgrade via fragmentation

"""
		self.assertEquals(results,expected_output)
		
	def testParseAnotherVersionString(self):
		# arrange
		parser = package_fetcher.ChangeLogParser()
		output = open('tests/complete_log.txt').read()
		
		# act
		results = parser.parse(output,'ca-certificates','2014.1.98','70.0.el7_0')
		
		# assert
		expected_output = """* Thu Sep 11 07:00:00 2014 Kai Engert <kaie@redhat.com> - 2014.1.98-70.0
- update to CKBI 1.98 from NSS 3.16.1
- building on RHEL 7 no longer requires java-openjdk
- added more detailed instructions for release numbers on RHEL branches,
  to avoid problems when rebasing on both z- and y-stream branches.

"""
		self.assertEquals(results,expected_output)
		
	def testNotFound(self):
		# arrange
		parser = package_fetcher.ChangeLogParser()
		output = open('tests/complete_log.txt').read()
		
		# act
		result = parser.parse(output,'bash','4.4','5.el7_0.4')
		
		# assert
		self.assertEquals(result,'Unable to parse changelog for package bash version 4.4 release 5.el7_0.4')

class PackageFetcherTestCase(unittest.TestCase):
	def testfetch_installed_packages(self):
		# arrange
		ch_log_parser = Mock()
		executor = Mock()
		fetcher = package_fetcher.PackageFetcher(ch_log_parser,executor)
		
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
		executor = Mock()
		fetcher = package_fetcher.PackageFetcher(ch_log_parser,executor)
		
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
		
	def testGetPackageChangeLogMock(self):
		# arrange
		ch_log_parser = Mock()
		ch_log_parser.parse = Mock(return_value='the changelog info')
		executor = Mock()
		executor.run_command = Mock(return_value='the raw output')
		fetcher = package_fetcher.PackageFetcher(ch_log_parser,executor)
		
		# act
		result = fetcher.get_package_changelog('bash', '1.2', '33')
		
		# assert
		self.assertEquals(result, 'the changelog info')
		
	def testGetPackageChangeLogRealBash(self):
		# arrange
		fetcher = package_fetcher.PackageFetcher(package_fetcher.ChangeLogParser(),mockable_execute.MockableExecute())

		# act
		result = fetcher.get_package_changelog('bash', '4.2.45', '5.el7_0.4')

		# assert
		self.assertNotEquals(result, None)
		
	def testGetPackageChangeLogRealOpenssl(self):
		# arrange
		fetcher = package_fetcher.PackageFetcher(package_fetcher.ChangeLogParser(),mockable_execute.MockableExecute())

		# act
		result = fetcher.get_package_changelog('openssl', '1.0.1e', '34.el7_0.4')

		# assert
		self.assertNotEquals(result, None)
		
if __name__ == "__main__":
            unittest.main()
