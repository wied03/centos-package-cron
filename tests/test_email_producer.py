import unittest
import sys
import os
from centos_package_cron.email_producer import *
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
        self.advisory_alerts_necessary = []
        self.annoyance_check_mock.is_advisory_alert_necessary = lambda advisory: advisory in self.advisory_alerts_necessary
        self.general_updates = []
        self.pkg_fetcher_mock.get_package_updates = lambda: self.general_updates
        
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
        raise 'write it'

    def test_produce_email_both_security_and_general_updates(self):
        raise 'write it'

    def test_produce_email_repo_excluded_and_included(self):
        raise 'write it'

    def test_produce_email_skip_old_turned_off(self):
        raise 'write it'
    
if __name__ == "__main__":
            unittest.main()