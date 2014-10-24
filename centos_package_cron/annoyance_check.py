from package import Package
from errata_item import ErrataItem
from sqlalchemy import or_

class AnnoyanceCheck:
    def __init__(self, session):
        self.session = session
    
    def is_advisory_alert_necessary(self, advisory):
        existing = self.session.query(ErrataItem).filter(ErrataItem.advisory_id == advisory.advisory_id).all()          
        if len(existing) == 0:
            self.session.add(advisory)
            self.session.commit()
            return True
        else:
            return False
    
    def is_package_alert_necessary(self, package):        
        existing = self.session.query(Package).filter(Package.name == package.name).all()            
        not_yet_notified = any(existing_package_notification.compare_evr(package) < 0 for existing_package_notification in existing)
        if len(existing) == 0 or not_yet_notified == True:
            self.session.add(package)
            self.session.commit()
            return True
        else:
            return False
                
    def remove_old_alerts_for_package(self, package):
        old_versions = self.session.query(Package) \
        .filter(Package.name == package.name) \
        .filter(or_(Package.version != package.version, Package.release != package.release)) \
        .all()
        
        for old_ver in old_versions:
            self.session.delete(old_ver)
            
        self.session.commit()       

    def remove_old_advisories(self, active_advisories):
        notified_advisories = self.session.query(ErrataItem).all()
        active_advisory_ids = map(lambda advisory: advisory.advisory_id, active_advisories)
        old_advisories = filter(lambda notified_advisory: notified_advisory.advisory_id not in active_advisory_ids, notified_advisories)
        for old_advisory in old_advisories:
            self.session.delete(old_advisory)
            
        self.session.commit()