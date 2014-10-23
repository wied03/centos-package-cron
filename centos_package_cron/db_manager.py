from package import Package

class DbManager:
    def __init__(self, session_fetcher):
        self.session_fetcher = session_fetcher    
    
    def is_package_alert_necessary(self, package):
        with self.session_fetcher as session:        
            existing = session.query(Package).filter(Package.name == package.name).all()            
            not_yet_notified = any(existing_package_notification.compare_evr(package) < 0 for existing_package_notification in existing)
            if len(existing) == 0 or not_yet_notified == True:
                session.add(package)
                session.commit()
                return True
            else:
                return False