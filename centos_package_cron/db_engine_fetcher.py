import sqlalchemy
from sqlite3 import dbapi2 as sqlite
from sqlalchemy.orm import sessionmaker
from db_base import Base

class DbEngineFetcher:
    def __init__(self, db_path='/var/lib/centos-package-cron/already_annoyed.sqlite'):
        self.db_path = db_path
        self.session = None
        
    def __enter__(self):
        engine = sqlalchemy.create_engine('sqlite:///%s' % (self.db_path),module=sqlite)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()        
        return self.session
        
    def __exit__(self, type, value, traceback):
        self.session.close()
                