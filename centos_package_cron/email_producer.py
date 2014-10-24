from annoyance_check import AnnoyanceCheck
from db_session_fetcher import db_session_fetcher
from package_fetcher import *
from package_checker import *
from errata_fetcher import *
from os_version_fetcher import *
from mockable_execute import *

class EmailProducer:
    def __init__(self, repos_to_exclude_list, repos_to_include_list, skip_old_notices):
        self.executor = MockableExecute()
        self.pkg_fetcher = PackageFetcher(ChangeLogParser(), self.executor, repos_to_exclude_list, repos_to_include_list)
        self.checker = PackageChecker(ErrataFetcher(), self.pkg_fetcher, OsVersionFetcher())
        self.annoyance_check = None
        self.skip_old_notices = skip_old_notices
        
    def _get_sorted_relevant_advisories(self):
        security_advisories = filter(lambda adv:adv['advisory'].type == ErrataType.SecurityAdvisory,self.checker.findAdvisoriesOnInstalledPackages())
        if self.skip_old_notices:
            only_advisories = map(lambda advpkg: advpkg['advisory'], security_advisories)
            self.annoyance_check.remove_old_advisories(only_advisories)
            security_advisories = filter(lambda advpkg: annoyance_check.is_advisory_alert_necessary(advpkg['advisory']))
            
        security_advisories = sorted(security_advisories, key=lambda adv: adv['advisory'].severity)
        
        return security_advisories
        
    def _add_advisories_to_email(self, security_advisories, email_body):
        if len(security_advisories) > 0:
            email_body += 'The following security advisories exist for installed packages:\n\n'
        for advisory_and_package in security_advisories:
            advisory = advisory_and_package['advisory']         
            email_body += "Advisory ID: %s\n" % (advisory.advisory_id)
            severity_label = ErrataSeverity.get_label(advisory.severity)
            email_body += "Severity: %s\n" % (severity_label)
            associated_package_labels = map(lambda pkg: "* %s-%s-%s" % (pkg.name, pkg.version, pkg.release),advisory_and_package['installed_packages'])
            # Remove dupes
            associated_package_labels = list(set(associated_package_labels))
            packages_flat = "\n".join(associated_package_labels)            
            email_body += "Packages:\n%s\n" % (packages_flat)
            references = map(lambda ref: "* %s" % (ref), advisory.references)
            references_flat = "\n".join(references)         
            email_body += "References:\n%s\n\n" % (references_flat)
            
        return email_body
        
    def _get_general_updates(self):
        return sorted(self.pkg_fetcher.get_package_updates(), key=lambda pkg: pkg.name)
        
    def _add_general_updates_to_email(self, general_updates, email_body):
        if len(general_updates) > 0:
            email_body += "The following packages are available for updating:\n\n"
            
        for update in general_updates:
            email_body += "%s-%s-%s from %s\n" % (update.name, update.version, update.release, update.repository)
            
        return email_body        
        
    def _add_changelogs_to_email(self, general_updates, email_body):
        if len(general_updates) > 0:
            changelogs = map(lambda pkg: { 'name': pkg.name, 'changelog': self.pkg_fetcher.get_package_changelog(pkg.name,pkg.version,pkg.release)},general_updates)
            email_body += "\n\nChange logs for available package updates:\n\n"
            
            for update in general_updates:
                changelog_entry = next(cl for cl in changelogs if cl['name'] == update.name)            
                email_body += "%s-%s-%s\n%s\n\n" % (update.name, update.version, update.release, changelog_entry['changelog'])
        
        return email_body
        
    def _handle_section_boundary(self, email_body):
        if email_body != '':
            return email_body + "\n"
        
    def produce_email(self):
        email_body = ''
        with db_session_fetcher() as session:
            self.annoyance_check = AnnoyanceCheck(session)
            advisories = self._get_sorted_relevant_advisories()            
            email_body = self._add_advisories_to_email(advisories, email_body)
            email_body = self._handle_section_boundary(email_body)
            general_updates = self._get_general_updates()
            email_body = self._add_general_updates_to_email(general_updates, email_body)
            email_body = self._handle_section_boundary(email_body)
            email_body = self._add_changelogs_to_email(general_updates, email_body)
            
        self.annoyance_check = None
        return email_body