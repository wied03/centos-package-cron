#!/usr/bin/python

import unittest
import sys
sys.path.append('../lib')
import errata_fetcher

class ErrataParserTest(unittest.TestCase):
	def testParseSingleRelease(self):
		# arrange
		parser = errata_fetcher.ErrataParser()
		xml = """
		<CEBA-2005--169 description="Not available" from="centos-announce@centos.org" issue_date="2005-04-07 01:27:35" notes="Not available" product="CentOS Linux" references="http://rhn.redhat.com/errata/RHBA-2005-169.html http://lists.centos.org/pipermail/centos-announce/2005-April/011555.html" release="1" solution="Not available" synopsis="CentOS and up2date - bugfix update" topic="Not available" type="Bug Fix Advisory">
		    <os_arch>i386</os_arch>
		    <os_arch>x86_64</os_arch>
		    <os_release>4</os_release>
		    <packages>up2date-gnome-4.4.5.6-2.centos4.i386.rpm</packages>
		    <packages>up2date-4.4.5.6-2.centos4.x86_64.rpm</packages>
		  </CEBA-2005--169>
		"""
		
		# act
		result = parser.parse(xml)
		
		# assert
		assert len(result) == 1
		first_advisory = result[0]
		assert isinstance(first_package, errata_fetcher.ErrataItem)
		assert first_advisory.advisory_id == 'CEBA-2005--169'
		assert first_advisory.type == errata_fetcher.ErrataType.BugFixAdvisory
		assert first_advisory.severity == None
		assert first_advisory.architectures == ['i386', 'x86_64']
		assert first_advisory.releases == ['4']
		assert first_advisory.packages == ['up2date-gnome-4.4.5.6-2.centos4.i386.rpm', 'up2date-4.4.5.6-2.centos4.x86_64.rpm']
		raise 'finish test'
		
	def testParseSeverityAvailable(self):
		# arrange
		
		# act
		
		# assert
		raise 'finish test'
		
	def testParseAllErrataTypes(self):
		# arrange
		
		# act
		
		# assert
		raise 'finish test'
		
	def testParseMultipleReleases(self):
		# arrange
		
		# act
		
		# assert
		raise 'finish test'
	
if __name__ == "__main__":
            unittest.main()