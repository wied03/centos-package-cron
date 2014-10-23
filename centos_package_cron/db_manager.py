from package import Package

class DbManager:
    def __init__(self, session_fetcher):
        self.session_fetcher = session_fetcher
    
    def is_package_alert_necessary(self, package):
        with self.session_fetcher as session:        
            existing = session.query(Package).filter(Package.name == package.name).all()
            if len(existing) == 0:
                session.add(package)
                session.commit()
                return True
            else:
                return False