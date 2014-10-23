from package import Package
from sqlalchemy import or_

class DbManager:
    def __init__(self, session):
        self.session = session
    
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