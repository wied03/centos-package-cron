#!/usr/bin/python

import unittest
import sys
import os
import os.path
from centos_package_cron.db_session_fetcher import db_session_fetcher
from centos_package_cron.db_base import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from subprocess import call

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
           
           
    def test_do_not_wipe_out_existing_db(self):
        # arrange
        row = DbSessionFetcherTest.Dummy(name='John Doe')
        with self.db_session_fetcher as session:
            # act
            session.add(row)
            session.commit()
            
        # act
        fetcher = db_session_fetcher(self.test_db_filename)
        row = DbSessionFetcherTest.Dummy(name='John Doe')
        with fetcher as session:
            session.add(row)
            session.commit()
            
            # assert
            query = session.query(DbSessionFetcherTest.Dummy).all()
            assert len(query) == 2
        
    def test_handles_directory_not_found(self):
        # arrange
        root_required_db_fetcher = db_session_fetcher('/var/directory_not_here/we_cant_access_this')

        # act
        try:
            with root_required_db_fetcher as session:               
                # assert
                fail('Expected exception here')
        except Exception as e:
            assert e.message == 'Unable to find a parent directory for DB /var/directory_not_here/we_cant_access_this, did you install properly?'        
           
    def test_handles_inability_to_create_file_in_directory(self):
        # arrange
        root_required_db_fetcher = db_session_fetcher('/var/we_cant_access_this')        
        
        # act
        try:
            with root_required_db_fetcher as session:
                # assert
                fail('Expected exception here')
        except Exception as e:
            assert e.message == 'Unable to write to directory for DB file /var/we_cant_access_this, do you need to run as root?'
            
    def test_handles_inability_to_edit_file_in_directory(self):
        # arrange
        try:
            call(['sudo', 'mkdir', '/var/we_cant_access_this'])
            call(['sudo', 'chown', 'vagrant', '/var/we_cant_access_this'])
            call(['sudo', 'touch', '/var/we_cant_access_this/db'])            

            root_required_db_fetcher = db_session_fetcher('/var/we_cant_access_this/db')        
        
            # act
            try:
                with root_required_db_fetcher as session:
                    # assert
                    fail('Expected exception here')
            except Exception as e:
                assert e.message == 'Unable to write to DB file /var/we_cant_access_this/db, do you need to run as root?'
        finally:
            call(['sudo', 'rm', '-rf', '/var/we_cant_access_this'])
    
if __name__ == "__main__":
            unittest.main()