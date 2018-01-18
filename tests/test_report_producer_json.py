# -*- coding: utf-8 -*-
import unittest
from centos_package_cron.report_producer import *
from centos_package_cron.package import *
from centos_package_cron.errata_item import *
from mock import Mock
import json

class db_session_fetcher_mock:        
    def __enter__(self):
        return "foo"
                
    def __exit__(self, type, value, traceback):
        howdy = 'howdy'                

class ReportProducerTest(unittest.TestCase):
    def setUp(self):
        self.pkg_fetcher_mock = Mock()
        self.pkg_checker_mock = Mock()
        self.annoyance_check_mock = Mock()
        self.annoy_fetcher_mock = Mock()
        self.annoy_fetcher_mock.fetch = Mock(return_value=self.annoyance_check_mock)
        self.db_session_mock = db_session_fetcher_mock()
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
        self.depends_on = {}
        self.pkg_fetcher_mock.get_what_depends_on = lambda name: self.depends_on[name]
        
    def get_producer(self,repo_exclude=[], repo_include=[], skip_old=True,include_depends_on=False):
        return ReportProducer(repo_exclude,
                             repo_include,
                             skip_old,
                             'doesnt matter',
                             self.pkg_fetcher_mock,
                             self.pkg_checker_mock,
                             self.annoy_fetcher_mock,
                             self.db_session_mock,
                             include_depends_on)

    def test_get_report_content_security_advisories_as_json(self):
        # arrange
        producer = self.get_producer()
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff'}
        advisory = ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['i686','x86_64'], ['7'], [{'name': 'libgcrypt','version':'1.5.3', 'release':'4.el7', 'arch':'x86_64'}],[])
        installed_packages = [package]
        self.advisories_on_installed = [{'advisory': advisory, 'installed_packages':installed_packages}]

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result)['advisories'] == [{"advisory_id": "adv id", "packages": ["libgcrypt-1.5.3-4.el7"], "severity": "Important"}]

    def test_get_report_content_general_updates_as_json(self):
        # arrange
        producer = self.get_producer()
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package]
        advisory = ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['i686','x86_64'], ['7'], [{'name': 'libgcrypt','version':'1.5.3', 'release':'4.el7', 'arch':'x86_64'}],[])
        installed_packages = [package]
        self.advisories_on_installed = [{'advisory': advisory, 'installed_packages':installed_packages}]

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result)['updates'] == [{"name":"libgcrypt-1.5.3-4.el7","source":"updates"}]

    def test_get_report_content_as_json_no_updates(self):
        # arrange
        producer = self.get_producer()

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {
            'advisories':[],
            'updates':[]
        }

    def test_get_report_content_as_json_no_updates_dependsonenabled(self):
        # arrange
        producer = self.get_producer(include_depends_on=True)

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {
            'advisories':[],
            'updates':[]
        }

    def test_get_report_content_as_json_general_but_no_security_advisories(self):
        # arrange
        producer = self.get_producer()
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff'}

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {
            'advisories':[],
            'updates':[{
                "name":"libgcrypt-1.5.3-4.el7",
                "source":"updates",
                "changelog": "stuff"
            }]
        }
        assert self.old_general_alerts_removed == [package]

    def test_get_report_content_as_json_general_but_no_security_advisories_depends_on_enabled(self):
        # arrange
        producer = self.get_producer(include_depends_on=True)
        package1 = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        package2 = Package('foo', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package1, package2]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff', ('foo', '1.5.3', '4.el7'): 'bah'}
        self.depends_on['libgcrypt'] = [Package('openssl', '1.2', '4.el7','x86_64', ''), Package('gnutls', '1.3', '4.el7','x86_64', '')]
        self.depends_on['foo'] = [Package('bah', '1.2', '4.el7','x86_64', '')]

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {
            'advisories':[],
            'updates':[
                {
                    "name":"foo-1.5.3-4.el7",
                    "source":"updates",
                    "required_by": ["bah"],
                    "changelog": "bah"
                },
                {
                    "name":"libgcrypt-1.5.3-4.el7",
                    "source":"updates",
                    "required_by": ["openssl","gnutls"],
                    "changelog": "stuff"
                }

            ]
        }

        assert self.old_general_alerts_removed == [package1, package2]

    def test_get_report_content_as_json_general_but_no_security_advisories_depends_on_enabled_and_some_packages_have_no_dependencies(self):
        # arrange
        producer = self.get_producer(include_depends_on=True)
        package1 = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        package2 = Package('foo', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package1, package2]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff', ('foo', '1.5.3', '4.el7'): 'bah'}
        self.depends_on['libgcrypt'] = []
        self.depends_on['foo'] = [Package('bah', '1.2', '4.el7','x86_64', '')]

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {
            'advisories':[],
            'updates':[
                {
                    "name":"foo-1.5.3-4.el7",
                    "source":"updates",
                    "required_by": ["bah"],
                    "changelog": "bah"
                },
                {
                    "name":"libgcrypt-1.5.3-4.el7",
                    "source":"updates",
                     "changelog": "stuff"
                }

            ]
        }

        assert self.old_general_alerts_removed == [package1, package2]

    def test_get_report_content_as_json_unicode_in_changelog(self):
        # arrange
        producer = self.get_producer()
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package]
        offending_changelog = '* Thu Aug 14 07:00:00 2014 Luk\xc3\xa1\xc5\xa1 Nykr\xc3\xbdn <lnykryn@redhat.com> - 9.49.17-1.1\n- fedora-readonly: fix prefix detection'
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): offending_changelog}

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {
        'advisories':[],
        'updates':[
            {
                "name":"libgcrypt-1.5.3-4.el7",
                "source":"updates",
                "changelog": u"* Thu Aug 14 07:00:00 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 9.49.17-1.1\n- fedora-readonly: fix prefix detection"
            }

        ]
    }

    def test_get_report_content_as_json_general_but_no_security_advisories_already_notified(self):
        # arrange
        producer = self.get_producer()
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff'}
        self.general_update_not_necessary = [package]

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {'advisories': [], 'updates': []}
        assert self.old_general_alerts_removed == []

    def test_get_report_content_as_json_both_security_and_general_updates(self):
        # arrange
        producer = self.get_producer()
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff'}
        advisory = ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['i686','x86_64'], ['7'], [{'name': 'libgcrypt','version':'1.5.3', 'release':'4.el7', 'arch':'x86_64'}],[])
        installed_packages = [package]
        self.advisories_on_installed = [{'advisory': advisory, 'installed_packages': installed_packages}]

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {
            'advisories':[{
                "advisory_id": "adv id",
                "packages": ["libgcrypt-1.5.3-4.el7"],
                "severity": "Important"}],
            'updates':[{
                "name":"libgcrypt-1.5.3-4.el7",
                "source":"updates",
                "changelog": "stuff"
            }]
        }
        assert self.old_advisories_removed_for_advisory_set == [[advisory]]
        assert self.old_general_alerts_removed == [package]

    def test_get_report_content_as_json_both_security_and_general_updates_already_notified(self):
        # arrange
        producer = self.get_producer()
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff'}
        advisory = ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['i686','x86_64'], ['7'], [{'name': 'libgcrypt','version':'1.5.3', 'release':'4.el7', 'arch':'x86_64'}],[])
        installed_packages = [package]
        self.advisories_on_installed = [{'advisory': advisory, 'installed_packages':installed_packages}]
        self.general_update_not_necessary = self.general_updates
        self.advisory_alerts_not_necessary = [advisory]

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {'advisories': [], 'updates': []}
        assert self.old_general_alerts_removed == []

    def test_get_report_content_as_json_both_security_and_some_general_updates_already_notified(self):
        # arrange
        producer = self.get_producer()
        package1 = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        package2 = Package('foo', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package1, package2]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff', ('foo', '1.5.3', '4.el7'): 'bah'}
        advisory = ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['i686','x86_64'], ['7'], [{'name': 'libgcrypt','version':'1.5.3', 'release':'4.el7', 'arch':'x86_64'}],[])
        installed_packages = [package1]
        self.advisories_on_installed = [{'advisory': advisory, 'installed_packages':installed_packages}]
        self.general_update_not_necessary = [package1]
        self.advisory_alerts_not_necessary = [advisory]

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {'advisories': [], 'updates': [
            {
                "name":"foo-1.5.3-4.el7",
                "source":"updates",
                "changelog": "bah"
            }
        ]}
        assert self.old_general_alerts_removed == [package2]

    def test_get_report_content_as_json_skip_old_turned_off(self):
        # arrange
        producer = self.get_producer(skip_old=False)
        package = Package('libgcrypt', '1.5.3', '4.el7', 'x86_64', 'updates')
        self.general_updates = [package]
        self.changelogs = {('libgcrypt', '1.5.3', '4.el7'): 'stuff'}
        advisory = ErrataItem('adv id', ErrataType.SecurityAdvisory,ErrataSeverity.Important, ['i686','x86_64'], ['7'], [{'name': 'libgcrypt','version':'1.5.3', 'release':'4.el7', 'arch':'x86_64'}],[])
        installed_packages = [package]
        self.advisories_on_installed = [{'advisory': advisory, 'installed_packages':installed_packages}]

        # act
        result = producer.get_report_content_as_json()

        # assert
        assert json.loads(result) == {
            'advisories':[{
                "advisory_id": "adv id",
                "packages": ["libgcrypt-1.5.3-4.el7"],
                "severity": "Important"}],
            'updates':[{
                "name":"libgcrypt-1.5.3-4.el7",
                "source":"updates",
                "changelog": "stuff"
            }]
        }

        assert self.old_general_alerts_removed == []
        assert self.old_advisories_removed_for_advisory_set == []

if __name__ == "__main__":
            unittest.main()