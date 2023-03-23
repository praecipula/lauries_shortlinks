#!/usr/bin/env python
import os

import logging
import python_logging_base

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref, declarative_base, sessionmaker
from sqlalchemy.sql import func

logger = logging.getLogger("models")
logger.setLevel(logging.DEBUG)

Base = declarative_base()

class SqlLiteHandler:

    DBFILENAME="matt_dot_directory.sqlite"

    @classmethod
    def initialize(cls):
        '''
        Create a new sqlite database based on our classes.
        '''
        # First, a sanity check: there should be a directory called "runners" in the current directory,
        # since we should always run all scripts with pwd = root of the repo.
        if not os.path.isdir("runners"):
            raise Exception("All scripts, especially ones that use data, need to run with `pwd` at the root of the repo")
        cls._engine = sqlalchemy.create_engine("sqlite:///runners/data/" + cls.DBFILENAME)
        Session = sessionmaker()
        Session.configure(bind=cls._engine)
        cls._session = Session()
        # This appears to be idempotent, at least for sqlite, so we'll call it every initialize.
        cls.create_tables()

    @classmethod
    def create_tables(cls):
        Base.metadata.create_all(cls._engine)

    @classmethod
    def session(cls):
        return cls._session

class RunLogSession(Base):
    '''
    Represents a RunLog, a time that a particular script is run and anything notable about the run.
    This is a one-to-many record of a log line.
    '''
    __tablename__ = "runlogsession"
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    logs = relationship("Log", backref=backref("runlogsession"))

    @classmethod
    def instance(cls):
        '''
        # As all runs should operate within a single RunLogSession, this is a singleton method to get the
        current session.
        '''
        if not hasattr(cls, '_current_session'):
            # Create and save
            cls._current_session = RunLogSession()
            SqlLiteHandler.session().add(cls._current_session)
            SqlLiteHandler.session().commit()
        return cls._current_session


class Log(Base):
    '''
    A not-performant, persisted, database-backed log.
    This should be used sparingly; it's not performant, and only used to possibly drive a UI /
    record summary of runs.
    '''

    __tablename__ = "runlog"
    id = Column(Integer, primary_key=True)
    logsession_id = Column(Integer, ForeignKey("runlogsession.id"))
    level = Column(String)
    name = Column(String)
    message = Column(String)

    @classmethod
    def info(cls, name, message):
        cls._create_log("info", name, message)

    def warn(cls, name, message):
        cls._create_log("warn", name, message)

    def error(cls, name, message):
        cls._create_log("err", name, message)
    
    @classmethod
    def _create_log(cls, level, name, message):
        l = Log(level=level, name=name, message=message, logsession_id = RunLogSession.instance().id)
        SqlLiteHandler.session().add(l)
        SqlLiteHandler.session().commit()



if __name__ == "__main__":
    print("Well, runs")
    SqlLiteHandler.initialize()
    Log.info("test", "I hope this works")
