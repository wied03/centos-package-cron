#!/usr/bin/python

import unittest
import sys
import os
import os.path
from centos_package_cron.db_session_fetcher import db_session_fetcher
from centos_package_cron.db_base import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey

class DbSessionFetcherTest(unittest.TestCase):
    class Dummy(Base):
        __tablename__ = 'dummy'
        id = Column(Integer, primary_key=True)
        name = Column(String(20))
        
        def __repr__(self):
            return "<Dummy(id='%s', name='%s')>" % (self.id, self.name)
    
    def remove(self):        
        if os.path.isfile(self.test_db_filename):
            os.remove(self.test_db_filename)
    
    def setUp(self):
        self.test_db_filename = 'test_db.sqlite'
        self.remove()     
        self.db_session_fetcher = db_session_fetcher(self.test_db_filename)
        
    def tearDown(self):
        self.remove()        
    
    def testCreatesSchemaWhenNoneExists(self):
        # arrange
        row = DbSessionFetcherTest.Dummy(name='John Doe')
        with self.db_session_fetcher as session:
            # act
            session.add(row)
            session.commit()
        
        with self.db_session_fetcher as session:
           # assert
           query = session.query(DbSessionFetcherTest.Dummy).all()
           assert len(query) == 1
           result = query[0]
           assert result.id == 1
           assert result.name == 'John Doe'    
    
if __name__ == "__main__":
            unittest.main()