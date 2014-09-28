#!/usr/bin/python

import unittest
import sys
from centos_package_cron import package_checker
from centos_package_cron import package_fetcher
from centos_package_cron import errata_fetcher
from centos_package_cron.errata_fetcher import ErrataType
from centos_package_cron.errata_fetcher import ErrataSeverity
from mock import Mock

class PackageCheckerTest(unittest.TestCase):
	def testSameVersionOfAnotherPackageInstalled(self):
		# arrange
		errata = Mock()
		errata.get_errata = Mock(return_value=[		
		errata_fetcher.ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['i686','x86_64'], ['7'], [{'name': 'libcacard-tools','version':'1.5.3', 'release':'60.el7_0.5', 'arch':'x86_64'}])
		])
		pkg = Mock()
		pkg.fetch_installed_packages = Mock(return_value=[
				package_fetcher.Package('libgcrypt', '1.5.3', '4.el7', 'x86_64')
		])
		os_fetcher = Mock()
		os_fetcher.get_top_level_version = Mock(return_value='7')
		checker = package_checker.PackageChecker(errata,pkg,os_fetcher)
		
		# act
		result = checker.findAdvisoriesOnInstalledPackages()
		
		# assert
		assert result == []
	
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
		xen_package = package_fetcher.Package('xen-libs','3.0.3', '135.el5_8.1', 'x86_64')
		pkg.fetch_installed_packages = Mock(return_value=[
		xen_package,
		package_fetcher.Package('openssl','2.0', '4.el7', 'x86_64')
		])
		os_fetcher = Mock()
		os_fetcher.get_top_level_version = Mock(return_value='7')
		checker = package_checker.PackageChecker(errata,pkg,os_fetcher)

		# act
		result = checker.findAdvisoriesOnInstalledPackages()

		# assert
		assert len(result) == 1
		first = result[0]
		assert first['advisory'] == advisory
		assert first['installed_packages'] == [xen_package]
		
	
if __name__ == "__main__":
            unittest.main()
