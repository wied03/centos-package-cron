#!/usr/bin/python

import unittest
import sys
import os
import os.path
from centos_package_cron import db_manager
from centos_package_cron import db_engine_fetcher

class DbManagerTest(unittest.TestCase):
    def setUp(self):
        test_db_filename = 'test_db.sqlite'
        if os.path.isfile(test_db_filename):
            os.remove(test_db_filename)
        self.db_engine_fetcher = db_engine_fetcher.DbEngineFetcher(test_db_filename)
    
    def testRecordPackageUpdateWithNoExisting(self):
        # arrange
        f = 'f'

if __name__ == "__main__":
            unittest.main()