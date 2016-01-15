import unittest
import pytest
import os
from centos_package_cron.os_version_fetcher import OsVersionFetcher

class TestOsVersionFetcher(unittest.TestCase):
    def testget_complete_version(self):
        # arrange
        checker = OsVersionFetcher()

        # act
        result = checker.get_complete_version()

        # assert
        expected = '6.6' if os.environ['DIMAGE'] == 'centos_cron_66' else '7.0.1406'
        self.assertEquals(result, expected)

    def testget_top_level_version(self):
        # arrange
        checker = OsVersionFetcher()

        # act
        result = checker.get_top_level_version()

        # assert
        expected = '6' if os.environ['DIMAGE'] == 'centos_cron_66' else '7'
        self.assertEquals(result, expected)

    def testget_mid_level_version(self):
        # arrange
        checker = OsVersionFetcher()

        # act
        result = checker.get_mid_level_version()

        # assert
        expected = '6.6' if os.environ['DIMAGE'] == 'centos_cron_66' else '7.0'
        self.assertEquals(result, expected)
