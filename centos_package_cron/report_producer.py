from annoyance_fetcher import AnnoyanceFetcher
from db_session_fetcher import db_session_fetcher
from package_fetcher import *
from package_checker import *
from errata_fetcher import *
from os_version_fetcher import *
from mockable_execute import *

class ReportProducer:
    def __init__(self,
                 repos_to_exclude_list,
                 repos_to_include_list,
                 skip_old_notices,
                 db_file_path,
                 pkg_fetcher=None,
                 checker=None,
                 annoyance_fetcher=None,
                 db_session_fetch=None,
                 include_depends_on=None):
        self.executor = MockableExecute()
        self.pkg_fetcher = pkg_fetcher or PackageFetcher(ChangeLogParser(), self.executor, repos_to_exclude_list, repos_to_include_list)
        self.checker = checker or PackageChecker(ErrataFetcher(), self.pkg_fetcher, OsVersionFetcher())
        self.annoyance_fetcher = annoyance_fetcher or AnnoyanceFetcher()
        self.db_session_fetch = db_session_fetch or db_session_fetcher(db_path=db_file_path)
        self.annoyance_check = None
        self.skip_old_notices = skip_old_notices
        self.include_depends_on = include_depends_on
        
    def _get_sorted_relevant_advisories(self):
        security_advisories = filter(lambda adv:adv['advisory'].type == ErrataType.SecurityAdvisory,self.checker.findAdvisoriesOnInstalledPackages())
        if self.skip_old_notices:
            only_advisories = map(lambda advpkg: advpkg['advisory'], security_advisories)
            self.annoyance_check.remove_old_advisories(only_advisories)
            security_advisories = filter(lambda advpkg: self.annoyance_check.is_advisory_alert_necessary(advpkg['advisory']), security_advisories)
            
        security_advisories = sorted(security_advisories, key=lambda adv: adv['advisory'].severity)
        
        return security_advisories
        
    def _add_advisories_to_email(self, security_advisories, email_body):
        if len(security_advisories) > 0:
            email_body += u'The following security advisories exist for installed packages:\n\n'
        for advisory_and_package in security_advisories:
            advisory = advisory_and_package['advisory']         
            email_body += u"Advisory ID: %s\n" % (advisory.advisory_id)
            severity_label = ErrataSeverity.get_label(advisory.severity)
            email_body += u"Severity: %s\n" % (severity_label)
            associated_package_labels = map(lambda pkg: "* %s-%s-%s" % (pkg.name, pkg.version, pkg.release),advisory_and_package['installed_packages'])
            # Remove dupes
            associated_package_labels = list(set(associated_package_labels))
            packages_flat = u"\n".join(associated_package_labels)            
            email_body += u"Packages:\n%s\n" % (packages_flat)
            references = map(lambda ref: u"* %s" % (ref), advisory.references)
            references_flat = u"\n".join(references)         
            email_body += u"References:\n%s\n\n" % (references_flat)
            
        return email_body
        
    def _get_general_updates(self):
        general_updates = self.pkg_fetcher.get_package_updates()
        if self.skip_old_notices:
            general_updates = filter(lambda pkg: self.annoyance_check.is_package_alert_necessary(pkg), general_updates)
            for update in general_updates:
                self.annoyance_check.remove_old_alerts_for_package(update)    

        return sorted(general_updates, key=lambda pkg: pkg.name)
        
    def _add_general_updates_to_email(self, general_updates, email_body):
        if len(general_updates) > 0:
            email_body += u"The following packages are available for updating:\n\n"
            
        for update in general_updates:
            email_body += u"%s-%s-%s from %s\n" % (update.name, update.version, update.release, update.repository)
            
        if self.include_depends_on:
            if len(general_updates) > 0:
                email_body += u"\n"
            for update in general_updates:
                depends_on = self.pkg_fetcher.get_what_depends_on(update.name)
                if len(depends_on) > 0:
                    email_body += u"These packages depend on %s:\n" % (update.name)
                    for depend in depends_on:
                        email_body += u"* %s\n" % (depend.name)                    
                    email_body += u"\n"
            
        return email_body        
        
    def _add_changelogs_to_email(self, general_updates, email_body):
        if len(general_updates) > 0:
            changelogs = map(lambda pkg: { 'name': pkg.name, 'changelog': self.pkg_fetcher.get_package_changelog(pkg.name,pkg.version,pkg.release)},general_updates)
            email_body += u"\n\nChange logs for available package updates:\n\n"
            
            for update in general_updates:
                changelog_entry = next(cl for cl in changelogs if cl['name'] == update.name)
                # Some log text is in unicode
                log_text = changelog_entry['changelog'].decode('utf-8')
                try:
                    email_body += u"%s-%s-%s\n%s\n\n" % (update.name, update.version, update.release, log_text)
                except:
                    print "Problem dealing with changelog entry %s" % (changelog_entry)                    
                    raise
        
        return email_body
        
    def _handle_section_boundary(self, email_body):
        if email_body != u'':
            email_body += u"\n"
        return email_body
        
    def get_report_content(self):
        email_body = u''
        with self.db_session_fetch as session:            
            self.annoyance_check = self.annoyance_fetcher.fetch(session)
            advisories = self._get_sorted_relevant_advisories()            
            email_body = self._add_advisories_to_email(advisories, email_body)
            email_body = self._handle_section_boundary(email_body)
            general_updates = self._get_general_updates()
            email_body = self._add_general_updates_to_email(general_updates, email_body)
            email_body = self._handle_section_boundary(email_body)
            email_body = self._add_changelogs_to_email(general_updates, email_body)
            
        self.annoyance_check = None
        return email_body