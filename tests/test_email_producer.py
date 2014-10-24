import unittest
import sys
import os
from centos_package_cron.email_producer import *
from mock import Mock

class EmailProducerTest(unittest.TestCase):
    def setUp(self):
        self.pkg_fetcher_mock = Mock()
        self.pkg_checker_mock = Mock()
        self.annoyance_check_mock = Mock()
        self.annoy_fetcher_mock = Mock()
        self.annoy_fetcher_mock.fetch = Mock(return_value=self.annoyance_check_mock)
        
    def get_producer(self,repo_exclude=[], repo_include=[], skip_old=True):
        return EmailProducer(repo_exclude, repo_include, skip_old, self.pkg_fetcher_mock, self.pkg_checker_mock, self.annoy_fetcher_mock)
        
    
    def test_produce_email_no_updates(self):
        raise 'write it'

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