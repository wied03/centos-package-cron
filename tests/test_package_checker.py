#!/usr/bin/python

import unittest
import sys
sys.path.append('../centos_package_cron')
import package_checker
import package_fetcher
import errata_fetcher
from errata_fetcher import ErrataType
from errata_fetcher import ErrataSeverity
from mock import Mock

class PackageCheckerTest(unittest.TestCase):
	def testFindAdvisoriesOnInstalledPackagesNotInstalled(self):
		# arrange		
		errata = Mock()
		errata.get_errata = Mock(return_value=[		
		errata_fetcher.ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['x86_64'], ['7'], [{'name': 'xen-libs','version':'3.0.3', 'release':'135.el5_8.2', 'arch':'x86_64'}])
		])
		pkg = Mock()
		pkg.fetch_installed_packages = Mock(return_value=[
		package_fetcher.Package('bash','1.0', '4.el7', 'x86_64'),
		package_fetcher.Package('openssl','2.0', '4.el7', 'x86_64')
		])
		os_fetcher = Mock()
		os_fetcher.get_top_level_version = Mock(return_value='7')
		checker = package_checker.PackageChecker(errata,pkg,os_fetcher)
		
		# act
		result = checker.findAdvisoriesOnInstalledPackages()
		
		# assert
		self.assertEquals(result, [])

	def testFindAdvisoriesOnInstalledPackagesInstalledButCurrentAlready(self):
		# arrange
		errata = Mock()
		errata.get_errata = Mock(return_value=[
		errata_fetcher.ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['x86_64'], ['7'], [{'name': 'xen-libs','version':'3.0.3', 'release':'135.el5_8.2', 'arch':'x86_64'}])
		])
		pkg = Mock()
		pkg.fetch_installed_packages = Mock(return_value=[
		package_fetcher.Package('xen-libs','3.0.3', '135.el5_8.2', 'x86_64'),
		package_fetcher.Package('openssl','2.0', '4.el7', 'x86_64')
		])
		os_fetcher = Mock()
		os_fetcher.get_top_level_version = Mock(return_value='7')
		checker = package_checker.PackageChecker(errata,pkg,os_fetcher)

		# act
		result = checker.findAdvisoriesOnInstalledPackages()

		# assert
		self.assertEquals(result, [])
	
	def testFindAdvisoriesOnInstalledPackagesInstalledButNewerVersion(self):
		# arrange
		errata = Mock()
		errata.get_errata = Mock(return_value=[
		errata_fetcher.ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['x86_64'], ['7'], [{'name': 'xen-libs','version':'3.0.3', 'release':'135.el5_8.2', 'arch':'x86_64'}])
		])
		pkg = Mock()
		pkg.fetch_installed_packages = Mock(return_value=[
		package_fetcher.Package('xen-libs','3.0.4', '135.el5_8.2', 'x86_64'),
		package_fetcher.Package('openssl','2.0', '4.el7', 'x86_64')
		])
		os_fetcher = Mock()
		os_fetcher.get_top_level_version = Mock(return_value='7')
		checker = package_checker.PackageChecker(errata,pkg,os_fetcher)

		# act
		result = checker.findAdvisoriesOnInstalledPackages()

		# assert
		self.assertEquals(result, [])
		
	def testFindAdvisoriesOnInstalledPackagesInstalledButLowerVersion(self):
		# arrange
		errata = Mock()
		errata.get_errata = Mock(return_value=[
		errata_fetcher.ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['x86_64'], ['7'], [{'name': 'xen-libs','version':'3.0.3', 'release':'135.el5_8.2', 'arch':'x86_64'}])
		])
		pkg = Mock()
		pkg.fetch_installed_packages = Mock(return_value=[
		package_fetcher.Package('xen-libs','3.0.2', '135.el5_8.2', 'x86_64'),
		package_fetcher.Package('openssl','2.0', '4.el7', 'x86_64')
		])
		os_fetcher = Mock()
		os_fetcher.get_top_level_version = Mock(return_value='7')
		checker = package_checker.PackageChecker(errata,pkg,os_fetcher)

		# act
		result = checker.findAdvisoriesOnInstalledPackages()

		# assert
		self.assertNotEquals(result, [])

	def testFindAdvisoriesOnInstalledPackagesInstalledButNewerRelease(self):
		# arrange
		errata = Mock()
		errata.get_errata = Mock(return_value=[
		errata_fetcher.ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['x86_64'], ['7'], [{'name': 'xen-libs','version':'3.0.3', 'release':'135.el5_8.2', 'arch':'x86_64'}])
		])
		pkg = Mock()
		pkg.fetch_installed_packages = Mock(return_value=[
		package_fetcher.Package('xen-libs','3.0.3', '135.el5_8.3', 'x86_64'),
		package_fetcher.Package('openssl','2.0', '4.el7', 'x86_64')
		])
		os_fetcher = Mock()
		os_fetcher.get_top_level_version = Mock(return_value='7')
		checker = package_checker.PackageChecker(errata,pkg,os_fetcher)

		# act
		result = checker.findAdvisoriesOnInstalledPackages()

		# assert
		self.assertEquals(result, [])
		
	def testFindAdvisoriesOnInstalledPackagesInstalledAndNeedsUpdatingButWrongCentOsVersion(self):
		# arrange
		errata = Mock()
		errata.get_errata = Mock(return_value=[
		errata_fetcher.ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['x86_64'], ['7'], [{'name': 'xen-libs','version':'3.0.3', 'release':'135.el5_8.2', 'arch':'x86_64'}])
		])
		pkg = Mock()
		pkg.fetch_installed_packages = Mock(return_value=[
		package_fetcher.Package('xen-libs','3.0.3', '135.el5_8.1', 'x86_64'),
		package_fetcher.Package('openssl','2.0', '4.el7', 'x86_64')
		])
		os_fetcher = Mock()
		os_fetcher.get_top_level_version = Mock(return_value='6')
		checker = package_checker.PackageChecker(errata,pkg,os_fetcher)

		# act
		result = checker.findAdvisoriesOnInstalledPackages()

		# assert
		self.assertEquals(result, [])
		
	def testFindAdvisoriesOnInstalledPackagesInstalledAndNeedsUpdating(self):
		# arrange
		errata = Mock()
		advisory = errata_fetcher.ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['x86_64'], ['7'], [{'name': 'xen-libs','version':'3.0.3', 'release':'135.el5_8.2', 'arch':'x86_64'}])
		errata.get_errata = Mock(return_value=[advisory])
		pkg = Mock()
		pkg.fetch_installed_packages = Mock(return_value=[
		package_fetcher.Package('xen-libs','3.0.3', '135.el5_8.1', 'x86_64'),
		package_fetcher.Package('openssl','2.0', '4.el7', 'x86_64')
		])
		os_fetcher = Mock()
		os_fetcher.get_top_level_version = Mock(return_value='7')
		checker = package_checker.PackageChecker(errata,pkg,os_fetcher)

		# act
		result = checker.findAdvisoriesOnInstalledPackages()

		# assert
		self.assertEquals(len(result),1)
		self.assertEquals(result[0],advisory)		
	
if __name__ == "__main__":
            unittest.main()
