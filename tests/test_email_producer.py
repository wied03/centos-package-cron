import unittest
import sys
import os
from centos_package_cron.email_producer import *
from centos_package_cron.package import *
from centos_package_cron.errata_item import *
from mock import Mock

class db_session_fetcher_mock:        
    def __enter__(self):
        return "foo"
                
    def __exit__(self, type, value, traceback):
        howdy = 'howdy'                

class EmailProducerTest(unittest.TestCase):
    def setUp(self):
        self.pkg_fetcher_mock = Mock()
        self.pkg_checker_mock = Mock()
        self.annoyance_check_mock = Mock()
        self.annoy_fetcher_mock = Mock()
        self.annoy_fetcher_mock.fetch = Mock(return_value=self.annoyance_check_mock)
        self.db_session_mock = db_session_fetcher_mock
        self.advisories_on_installed = []
        self.pkg_checker_mock.findAdvisoriesOnInstalledPackages = lambda: self.advisories_on_installed
        self.advisory_alerts_not_necessary = []        
        self.annoyance_check_mock.is_advisory_alert_necessary = lambda advisory: advisory not in self.advisory_alerts_not_necessary
        self.general_update_not_necessary = []
        self.annoyance_check_mock.is_package_alert_necessary = lambda package: package not in self.general_update_not_necessary
        self.old_advisories_removed_for_advisory_set = []
        self.annoyance_check_mock.remove_old_advisories = lambda active_ad: self.old_advisories_removed_for_advisory_set.append(active_ad)
        self.old_general_alerts_removed = []
        self.annoyance_check_mock.remove_old_alerts_for_package = lambda package: self.old_general_alerts_removed.append(package)
        self.general_updates = []
        self.pkg_fetcher_mock.get_package_updates = lambda: self.general_updates
        self.changelogs = {}
        self.pkg_fetcher_mock.get_package_changelog = lambda name,vers,release: self.changelogs[(name,vers,release)]
        
    def get_producer(self,repo_exclude=[], repo_include=[], skip_old=True):
        return EmailProducer(repo_exclude,
                             repo_include,
                             skip_old,
                             self.pkg_fetcher_mock,
                             self.pkg_checker_mock,
                             self.annoy_fetcher_mock,
                             self.db_session_mock)        
    
    def test_produce_email_no_updates(self):
        # arrange
        producer = self.get_producer()
        
        # act
        result = producer.produce_email()
        
        # assert
        assert result == ''

    def test_produce_email_general_but_no_security_advisories(self):
        # arrange
        producer = self.get_producer()
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff'}
        
        # act
        result = producer.produce_email()
        
        # assert
        assert result == """The following packages are available for updating:

libgcrypt-1.5.3-4.el7 from updates



Change logs for available package updates:

libgcrypt-1.5.3-4.el7
stuff

"""
        assert self.old_general_alerts_removed == [[package]]
        
    def test_produce_email_general_but_no_security_advisories_already_notified(self):
        # arrange
        producer = self.get_producer()
        self.general_updates = [Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff'}
        self.general_update_not_necessary = self.general_updates
        
        # act
        result = producer.produce_email()
        
        # assert
        assert result == ''
        assert self.old_general_alerts_removed == []   

    def test_produce_email_both_security_and_general_updates(self):
        # arrange
        producer = self.get_producer()
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff'}
        advisory = ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['i686','x86_64'], ['7'], [{'name': 'libgcrypt','version':'1.5.3', 'release':'4.el7', 'arch':'x86_64'}],[])
        installed_packages = [package]
        self.advisories_on_installed = [{'advisory': advisory, 'installed_packages':installed_packages}]
        
        # act
        result = producer.produce_email()
        
        # assert
        assert result == """The following security advisories exist for installed packages:

Advisory ID: adv id
Severity: Important
Packages:
* libgcrypt-1.5.3-4.el7
References:



The following packages are available for updating:

libgcrypt-1.5.3-4.el7 from updates



Change logs for available package updates:

libgcrypt-1.5.3-4.el7
stuff

"""
        assert self.old_advisories_removed_for_advisory_set == [[advisory]]
        assert self.old_general_alerts_removed == [[package]]
        
    def test_produce_email_both_security_and_general_updates_already_notified(self):
        raise 'write it'
        
    def test_produce_email_repo_excluded_and_included(self):
        raise 'write it'

    def test_produce_email_skip_old_turned_off(self):
        raise 'write it'
    
if __name__ == "__main__":
            unittest.main()