import sqlalchemy
from sqlite3 import dbapi2 as sqlite
from sqlalchemy.orm import sessionmaker
from db_base import Base
import os

class db_session_fetcher:
    DEFAULT_DB_PATH = '/var/lib/centos-package-cron/already_annoyed.sqlite'
    
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        self.session = None
        self.engine = None
        
    def __enter__(self):
        if self.engine == None:
            absolute_path = os.path.abspath(self.db_path)
            parent_dir = os.path.dirname(absolute_path)
            if not os.path.exists(parent_dir):
                raise Exception("Unable to find a parent directory for DB %s, did you install properly?" % (absolute_path))
                
            if not os.access(parent_dir, os.W_OK):
                raise Exception("Unable to write to directory for DB file %s, do you need to run as root?" % (absolute_path))
                
            if os.path.exists(absolute_path) and not os.access(absolute_path, os.W_OK):
                raise Exception("Unable to write to DB file %s, do you need to run as root?" % (absolute_path))
                
            self.engine = sqlalchemy.create_engine('sqlite:///%s' % (self.db_path),module=sqlite)
            
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()        
        return self.session
        
    def __exit__(self, type, value, traceback):
        self.session.close()
                