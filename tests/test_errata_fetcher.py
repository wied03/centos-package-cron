#!/usr/bin/python

import unittest
import sys
sys.path.append('../lib')
import errata_fetcher
from errata_fetcher import ErrataType

class ErrataParserTest(unittest.TestCase):
	def testParseSingleRelease(self):
		# arrange
		parser = errata_fetcher.ErrataParser()
		xml = """
		<opt>
		<CEBA-2005--169 description="Not available" from="centos-announce@centos.org" issue_date="2005-04-07 01:27:35" notes="Not available" product="CentOS Linux" references="http://rhn.redhat.com/errata/RHBA-2005-169.html http://lists.centos.org/pipermail/centos-announce/2005-April/011555.html" release="1" solution="Not available" synopsis="CentOS and up2date - bugfix update" topic="Not available" type="Bug Fix Advisory">
		    <os_arch>i386</os_arch>
		    <os_arch>x86_64</os_arch>
		    <os_release>4</os_release>
		    <packages>up2date-gnome-4.4.5.6-2.centos4.i386.rpm</packages>
		    <packages>up2date-4.4.5.6-2.centos4.x86_64.rpm</packages>
		  </CEBA-2005--169>
		</opt>
		"""
		
		# act
		result = parser.parse(xml)
		
		# assert
		self.assertEqual(len(result),1)
		first_advisory = result[0]
		assert isinstance(first_advisory, errata_fetcher.ErrataItem)
		assert first_advisory.advisory_id == 'CEBA-2005--169'
		self.assertEquals(first_advisory.type, ErrataType.BugFixAdvisory)
		self.assertEquals(first_advisory.severity, None)
		self.assertEquals(first_advisory.architectures, ['i386', 'x86_64'])
		self.assertEquals(first_advisory.releases, ['4'])
		expected_packages = [
		{'name': 'up2date-gnome',
		'version': '4.4.5.6',
		'release': '2.centos4',
		'arch':'i386'},
		{'name': 'up2date',
		'version': '4.4.5.6',
		'release': '2.centos4',
		'arch':'x86_64'}		
		]
		self.assertEquals(first_advisory.packages, expected_packages)
		
	def testParseIgnoresMeta(self):
		# arrange
		parser = errata_fetcher.ErrataParser()
		xml = """
		<opt>
		<CEBA-2005--169 description="Not available" from="centos-announce@centos.org" issue_date="2005-04-07 01:27:35" notes="Not available" product="CentOS Linux" references="http://rhn.redhat.com/errata/RHBA-2005-169.html http://lists.centos.org/pipermail/centos-announce/2005-April/011555.html" release="1" solution="Not available" synopsis="CentOS and up2date - bugfix update" topic="Not available" type="Bug Fix Advisory">
		    <os_arch>i386</os_arch>
		    <os_arch>x86_64</os_arch>
		    <os_release>4</os_release>
		    <packages>up2date-gnome-4.4.5.6-2.centos4.i386.rpm</packages>
		    <packages>up2date-4.4.5.6-2.centos4.x86_64.rpm</packages>
		  </CEBA-2005--169>
		<meta>
		    <author>Steve Meier</author>
		    <license>Free for non-commercial use</license>
		    <disclaimer>This software is provided AS IS. There are no guarantees. It might kill your cat.</disclaimer>
		    <timestamp>Fri Sep 26 07:39:11 UTC 2014</timestamp>
		  </meta>
		</opt>
		"""
		
		# act
		result = parser.parse(xml)
		
		# assert
		self.assertEqual(len(result),1)
		first_advisory = result[0]
		assert isinstance(first_advisory, errata_fetcher.ErrataItem)
		
	def testParseSeverityAvailable(self):
		# arrange
		parser = errata_fetcher.ErrataParser()
		xml = """
		<opt>
		<CEBA-2005--169 description="Not available" from="centos-announce@centos.org" issue_date="2005-04-07 01:27:35" notes="Not available" product="CentOS Linux" references="http://rhn.redhat.com/errata/RHBA-2005-169.html http://lists.centos.org/pipermail/centos-announce/2005-April/011555.html" release="1" solution="Not available" synopsis="CentOS and up2date - bugfix update" topic="Not available" severity="Important" type="Bug Fix Advisory">
		    <os_arch>i386</os_arch>
		    <os_arch>x86_64</os_arch>
		    <os_release>4</os_release>
		    <packages>up2date-gnome-4.4.5.6-2.centos4.i386.rpm</packages>
		    <packages>up2date-4.4.5.6-2.centos4.x86_64.rpm</packages>
		  </CEBA-2005--169>
		</opt>
		"""
		
		# act
		result = parser.parse(xml)
		
		# assert
		self.assertEqual(len(result),1)
		first_advisory = result[0]
		assert isinstance(first_advisory, errata_fetcher.ErrataItem)
		assert first_advisory.advisory_id == 'CEBA-2005--169'
		self.assertEquals(first_advisory.type, ErrataType.BugFixAdvisory)
		self.assertEquals(first_advisory.severity, errata_fetcher.ErrataSeverity.Important)
		self.assertEquals(first_advisory.architectures, ['i386', 'x86_64'])
		self.assertEquals(first_advisory.releases, ['4'])
		expected_packages = [
		{'name': 'up2date-gnome',
		'version': '4.4.5.6',
		'release': '2.centos4',
		'arch':'i386'},
		{'name': 'up2date',
		'version': '4.4.5.6',
		'release': '2.centos4',
		'arch':'x86_64'}		
		]
		self.assertEquals(first_advisory.packages, expected_packages)
		
	def testParseAllErrataTypes(self):
		# arrange
		possible_values = ['Bug Fix Advisory','Security Advisory','Product Enhancement Advisory']
		parser = errata_fetcher.ErrataParser()
		
		# act + assert
		for string in possible_values:
			self.assertNotEquals(parser.getType(string), None)		
		
	def testParseAllErrataSeverities(self):
		# arrange
		possible_values = ['Important', 'Moderate', 'Low', 'Critical']
		parser = errata_fetcher.ErrataParser()
		
		# act + assert
		for string in possible_values:
			self.assertNotEquals(parser.getSeverity(string), None)
			
class ErrataFetcherTest(unittest.TestCase):
	def testFetch(self):
		# arrange
		fetcher = errata_fetcher.ErrataFetcher()
		
		# act
		result = fetcher.get_errata()
		
		# assert
		self.assertGreater(len(result),0)
	
if __name__ == "__main__":
            unittest.main()