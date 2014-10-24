#!/usr/bin/python

import unittest
import sys
import os
import os.path
from centos_package_cron.annoyance_check import AnnoyanceCheck
from centos_package_cron.db_session_fetcher import db_session_fetcher
from centos_package_cron.package import Package
from centos_package_cron.errata_item import *

class AnnoyanceCheckTest(unittest.TestCase):
    def remove(self):        
        if os.path.isfile(self.test_db_filename):
            os.remove(self.test_db_filename)
    
    def setUp(self):
        self.test_db_filename = 'test_db.sqlite'
        self.remove()
        self.session_fetcher = db_session_fetcher(self.test_db_filename)
        self.session = self.session_fetcher.__enter__()
        self.annoyance_check = AnnoyanceCheck(self.session)
        
    def tearDown(self):
        self.session_fetcher.__exit__(None,None,None)
    
    def test_is_package_alert_necessary_no_existing_notices(self):
        # arrange
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')

        # act
        result = self.annoyance_check.is_package_alert_necessary(package)

        # assert
        assert result == True
        
    def test_is_package_alert_necessary_existing_notice_already_in_place(self):
        # arrange
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.annoyance_check.is_package_alert_necessary(package)
        # session/bound
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        
        # act
        result = self.annoyance_check.is_package_alert_necessary(package)
        
        # assert
        assert result == False
        
    def test_is_package_alert_necessary_notice_in_place_but_older_version(self):
        # arrange
        existing_notice = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.annoyance_check.is_package_alert_necessary(existing_notice)
        new_notice = Package('libgcrypt', '1.5.4', '4.el7', 'x86_64', 'updates')

        # act
        result = self.annoyance_check.is_package_alert_necessary(new_notice)

        # assert
        assert result == True

    def test_is_package_alert_necessary_notice_in_place_but_older_release(self):
        # arrange
        existing_notice = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.annoyance_check.is_package_alert_necessary(existing_notice)
        new_notice = Package('libgcrypt', '1.5.3', '5.el7', 'x86_64', 'updates')

        # act
        result = self.annoyance_check.is_package_alert_necessary(new_notice)

        # assert
        assert result == True
        
    def test_remove_old_alerts_for_package_with_new_version(self):
        # arrange
        existing_notice = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.annoyance_check.is_package_alert_necessary(existing_notice)
        new_notice = Package('libgcrypt', '1.5.4', '4.el7', 'x86_64', 'updates')
        self.annoyance_check.is_package_alert_necessary(new_notice)
        
        # act
        self.annoyance_check.remove_old_alerts_for_package(new_notice)
        
        # assert
        results = self.session.query(Package).all()
        
        assert len(results) == 1
        result = results[0]
        assert result.name == 'libgcrypt'
        assert result.version == '1.5.4'
        assert result.release == '4.el7'
        assert result.arch == 'x86_64'
        assert result.repository == 'updates'
        assert result.timestamp != None
        
    def test_remove_old_alerts_for_package_with_new_release(self):
        # arrange
        existing_notice = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.annoyance_check.is_package_alert_necessary(existing_notice)
        new_notice = Package('libgcrypt', '1.5.3', '5.el7', 'x86_64', 'updates')
        self.annoyance_check.is_package_alert_necessary(new_notice)
        
        # act
        self.annoyance_check.remove_old_alerts_for_package(new_notice)
        
        # assert
        results = self.session.query(Package).all()
        
        assert len(results) == 1
        result = results[0]
        assert result.name == 'libgcrypt'
        assert result.version == '1.5.3'
        assert result.release == '5.el7'
        assert result.arch == 'x86_64'
        assert result.repository == 'updates'
        
    def test_is_advisory_alert_necessary_no_existing_notices(self):
        # arrange
        advisory = ErrataItem(advisory_id='CVE-123', type=ErrataType.BugFixAdvisory, severity=ErrataSeverity.Important, architectures=['x86_64'], releases=['5'], packages=[{'name': 'libcacard-tools','version':'1.5.3', 'release':'60.el7_0.5', 'arch':'x86_64'}], references=[])
        
        # act
        result = self.annoyance_check.is_advisory_alert_necessary(advisory)
        
        # assert
        assert result == True
        
    def test_is_advisory_alert_necessary_already_there(self):
        # arrange
        advisory = ErrataItem(advisory_id='CVE-123', type=ErrataType.BugFixAdvisory, severity=ErrataSeverity.Important, architectures=['x86_64'], releases=['5'], packages=[{'name': 'libcacard-tools','version':'1.5.3', 'release':'60.el7_0.5', 'arch':'x86_64'}], references=[])
        self.annoyance_check.is_advisory_alert_necessary(advisory)
        # session/bound
        advisory = ErrataItem(advisory_id='CVE-123', type=ErrataType.BugFixAdvisory, severity=ErrataSeverity.Important, architectures=['x86_64'], releases=['5'], packages=[{'name': 'libcacard-tools','version':'1.5.3', 'release':'60.el7_0.5', 'arch':'x86_64'}], references=[])
        
        # act
        result = self.annoyance_check.is_advisory_alert_necessary(advisory)
        
        # assert
        assert result == False

if __name__ == "__main__":
            unittest.main()