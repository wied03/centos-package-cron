import unittest
import pytest
from centos_package_cron.os_version_fetcher import OsVersionFetcher

class TestOsVersionFetcher(unittest.TestCase):
    def testget_complete_version(self):
        # arrange
        checker = OsVersionFetcher()
        
        # act
        result = checker.get_complete_version()
        
        # assert
        self.assertEquals(result, '7.0.1406')
        
    def testget_top_level_version(self):
        # arrange
        checker = OsVersionFetcher()

        # act
        result = checker.get_top_level_version()

        # assert
        self.assertEquals(result, '7')
