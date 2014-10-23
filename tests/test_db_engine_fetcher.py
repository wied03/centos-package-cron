#!/usr/bin/python

import unittest
import sys
import os
import os.path
from centos_package_cron.db_engine_fetcher import DbEngineFetcher
from centos_package_cron.db_base import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey

class DbEngineFetcherTest(unittest.TestCase):
    class Dummy(Base):
        __tablename__ = 'dummy'
        id = Column(Integer, primary_key=True)
        name = Column(String(20))
        
        def __repr__(self):
            return "<Dummy(id='%s', name='%s')>" % (self.id, self.name)
    
    def setUp(self):
        test_db_filename = 'test_db.sqlite'
        if os.path.isfile(test_db_filename):
            os.remove(test_db_filename)
        self.db_engine_fetcher = DbEngineFetcher(test_db_filename)
    
    def testCreatesSchemaWhenNoneExists(self):
        # arrange
        row = DbEngineFetcherTest.Dummy(name='John Doe')
        with self.db_engine_fetcher as session:
            # act
            session.add(row)
            session.commit()
        
        with self.db_engine_fetcher as session:
           # assert
           result = session.query(DbEngineFetcherTest.Dummy)[0]
           assert result.id == 1
           assert result.name == 'John Doe'
    
    def testDoesNotDisturbExistingData(self):
        assert True == False

if __name__ == "__main__":
            unittest.main()