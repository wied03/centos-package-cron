#!/usr/bin/python

import unittest
import sys
import os
import os.path
from centos_package_cron.db_manager import DbManager
from centos_package_cron.db_session_fetcher import db_session_fetcher
from centos_package_cron.package import Package

class DbManagerTest(unittest.TestCase):
    def remove(self):        
        if os.path.isfile(self.test_db_filename):
            os.remove(self.test_db_filename)
    
    def setUp(self):
        self.test_db_filename = 'test_db.sqlite'
        self.remove()     
        self.db_manager = DbManager(db_session_fetcher(self.test_db_filename))
        
    def tearDown(self):
        self.remove()
    
    def test_is_package_alert_necessary_no_existing_notices(self):
        # arrange
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        
        # act
        result = self.db_manager.is_package_alert_necessary(package)
        
        # assert
        assert result == True
        # session/bound
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        try2 = self.db_manager.is_package_alert_necessary(package)
        assert try2 == False

if __name__ == "__main__":
            unittest.main()