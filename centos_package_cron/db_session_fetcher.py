import sqlalchemy
from sqlite3 import dbapi2 as sqlite
from sqlalchemy.orm import sessionmaker
from db_base import Base

class db_session_fetcher:
    DEFAULT_DB_PATH = '/var/lib/centos-package-cron/already_annoyed.sqlite'
    
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        self.session = None
        self.engine = None
        
    def __enter__(self):
        if self.engine == None:
            try:
                with open(name=self.db_path, mode='w') as f:
                    foo = 'hi'
            except IOError as e:
                if e.errno == 2:
                    raise Exception("Unable to find a parent directory for DB %s, did you install properly?" % (self.db_path))
                if e.errno == 13:
                    raise Exception("Unable to write to DB file %s, do you need to run as root?" % (self.db_path))
                raise
                
            self.engine = sqlalchemy.create_engine('sqlite:///%s' % (self.db_path),module=sqlite)
            
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()        
        return self.session
        
    def __exit__(self, type, value, traceback):
        self.session.close()
                