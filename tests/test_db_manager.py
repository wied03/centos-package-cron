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
    
    def test_is_package_alert_necessary_no_existing_notices(self):
        # arrange
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')

        # act
        result = self.db_manager.is_package_alert_necessary(package)

        # assert
        assert result == True
        
    def test_is_package_alert_necessary_existing_notice_already_in_place(self):
        # arrange
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.db_manager.is_package_alert_necessary(package)
        # session/bound
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        
        # act
        result = self.db_manager.is_package_alert_necessary(package)
        
        # assert
        assert result == False
        
    def test_is_package_alert_necessary_notice_in_place_but_older_version(self):
        # arrange
        existing_notice = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.db_manager.is_package_alert_necessary(existing_notice)
        new_notice = Package('libgcrypt', '1.5.4', '4.el7', 'x86_64', 'updates')

        # act
        result = self.db_manager.is_package_alert_necessary(new_notice)

        # assert
        assert result == True

    def test_is_package_alert_necessary_notice_in_place_but_older_release(self):
        # arrange
        existing_notice = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.db_manager.is_package_alert_necessary(existing_notice)
        new_notice = Package('libgcrypt', '1.5.3', '5.el7', 'x86_64', 'updates')

        # act
        result = self.db_manager.is_package_alert_necessary(new_notice)

        # assert
        assert result == True

if __name__ == "__main__":
            unittest.main()