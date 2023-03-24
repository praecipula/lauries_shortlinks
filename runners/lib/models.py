#!/usr/bin/env python
import os
import re

import logging
import python_logging_base
import google_cloud_storage

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Index, event, select
from sqlalchemy.orm import relationship, backref, declarative_base, sessionmaker
from sqlalchemy.sql import func, expression

logger = logging.getLogger("models")
logger.setLevel(logging.DEBUG)

Base = declarative_base()

class SqlLiteHandler:

    DBFILENAME="matt_dot_directory.sqlite"
    FILEPATH="runners/data/" + DBFILENAME

    @classmethod
    def download(cls):
        try:
            google_cloud_storage.download(SqlLiteHandler.DBFILENAME, SqlLiteHandler.FILEPATH)
        except google_cloud_storage.NotFound:
            logger.warning("No database file found in GCStorage. The one on the filesystem, or a new one, will be used on initialize.")

    @classmethod
    def idempotent_download(cls):
        if not os.path.isfile(SqlLiteHandler.FILEPATH):
            cls.download()

    @classmethod
    def upload(cls):
        try:
            google_cloud_storage.upload(SqlLiteHandler.DBFILENAME, SqlLiteHandler.FILEPATH)
        except:
            logger.error("Failed to upload to GCStorage. The data from this run will be LOST.")
            raise


    @classmethod
    def initialize(cls):
        '''
        Create a new sqlite database based on our classes.
        '''
        # First, a sanity check: there should be a directory called "runners" in the current directory,
        # since we should always run all scripts with pwd = root of the repo.
        if not os.path.isdir("runners"):
            raise Exception("All scripts, especially ones that use data, need to run with `pwd` at the root of the repo")
        cls._engine = sqlalchemy.create_engine("sqlite:///" + cls.FILEPATH, echo=True)
        Session = sessionmaker()
        Session.configure(bind=cls._engine)
        cls._session = Session()
        # This appears to be idempotent, at least for sqlite, so we'll call it every initialize.
        cls.create_tables()

    @classmethod
    def idempotent_initialize(cls):
        if not hasattr(cls, "_session"):
            cls.initialize()

    @classmethod
    def create_tables(cls):
        Base.metadata.create_all(cls._engine)

    @classmethod
    def session(cls):
        if not hasattr(cls, "_session"):
            raise Exception("SqlLiteHandler has no session set; did you call initialize()?")
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
    record summary of runs and to do data analysis over time.
    '''

    __tablename__ = "runlog"
    id = Column(Integer, primary_key=True)
    logsession_id = Column(Integer, ForeignKey("runlogsession.id"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
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

class LPage(Base):
    '''
    Basic page data for a shortlink page. This is largely the key on which to join other metadata (a screenshot of the page
    that's saved in GCStorage, 
    '''
    __tablename__ = "page"
    id = Column(Integer, primary_key=True)
    # This is the path to the _file on filesystem_, relative to the repo root, not the path as served.
    path = Column(String, nullable=False)
    trashed = Column(Boolean, nullable=False, server_default=expression.false())

    page_metadata = relationship("PageMetadata", backref=backref("page"))

    __table_args__ = (
            Index('page_path_index', 'path'),
            )

    @classmethod
    def normalize_page_path(cls, pathname):
        fullpath = os.path.abspath(pathname)
        matches=re.search(".*\/l\/(?P<normpath>.*)", fullpath)
        return matches.group('normpath')

    @classmethod
    def find_by_path(cls, path):
        norm_path = cls.normalize_page_path(path)
        q = select(LPage).where(LPage.trashed == False). \
                where(LPage.path==norm_path).limit(2)
        pages = list(SqlLiteHandler.session().execute(q))
        python_logging_base.ASSERT(len(pages) <= 1, f"Expected exactly one page for path {norm_path}, got {len(pages)}")
        if len(pages) == 0:
            return None
        return pages[0]

    @classmethod
    def upsert(cls, path):
        '''
        For now, this is implemented in Python logic, which is race-condition-y, but I don't care because that's edge casey enough
        to accept. I don't even know if sqlite has an upsert...

        Also, page doesn't have much data to update, but it might in the future.
        '''
        instance = cls.find_by_path(path)
        if not instance:
            # Yes, we'll normalize twice with doing this again after find_by_path, but only on first create, so meh.
            norm_path = cls.normalize_page_path(path)
            instance = LPage(path=norm_path)
            SqlLiteHandler.session().add(instance)
            SqlLiteHandler.session().commit()
        return instance

    def __repr__(self):
        return f"<LPage(path='{self.path}', trashed={self.trashed}>"



# NB: This is top-level again, not a member of LPage.
@event.listens_for(LPage.path, 'set', retval=True)
def normalize_page_path_event_handler(target, pathname, oldpathname, initiator):
    return LPage.normalize_page_path(pathname)

class PageMetadata(Base):
    '''
    Metadata about a page. This is a simple k/v store for data that connects to a page; often done with frontmatter,
    but can also contain other metadata that's done out of band, for instance, tracking last page changes and whatnot.
    '''
    __tablename__ = "page_metadata"
    id = Column(Integer, primary_key=True)
    key = Column(String(100), nullable=False)
    value = Column(String)
    time_refreshed = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    trashed = Column(Boolean, nullable=False, server_default=expression.false())
    page_id = Column(Integer, ForeignKey("page.id"))

    @classmethod
    def find_all_by_page(cls, page):
        q = select(PageMetadata).where(PageMetadata.trashed == False). \
            where(PageMetadata.page_id==page.id).limit(200)
        return list(SqlLiteHandler.session().execute(q))

    @classmethod
    def upsert_or_trash_all_by_page(cls, page, attr_dict):
        '''
        This will make the DB "look like" what's in the repo; that is:
        * If it's in the attr_dict but not the DB, insert it
        * If it's in the attr_dict and the DB, update it
        * If it's not in the attr_dict and in the DB, trash it.
        '''

        # Find all including trashed; we can untrash if we see it again
        q = select(PageMetadata).where(PageMetadata.page_id==page.id).limit(200)
        existing_meta = list(SqlLiteHandler.session().execute(q))
        for (db_meta,) in existing_meta:
            fmtr_value = attr_dict.get(db_meta.key)
            if fmtr_value == None:
                logger.debug("{self} exists in the DB but not in frontmatter; trashing")
                db_meta.trashed = True
            else:
                # Exists in both DB and db_meta_dict; ensure untrashed and update; remove from dict
                logger.debug("{self} exists in the DB and in frontmatter; updating")
                db_meta.trashed = False
                db_meta.value = fmtr_value
                del attr_dict[db_meta.key]
        # Now anything left in attr_dict is not in the DB.
        for fmtr_key, fmtr_value in attr_dict.items():
            logger.debug("{fmtr_key}: {fmtr_value} does not exist in the DB, adding")
            new_meta = PageMetadata(key=fmtr_key, value=fmtr_value, page_id = page.id)
            SqlLiteHandler.session().add(new_meta)
        # Commit all our changes
        SqlLiteHandler.session().commit()

    def __repr__(self):
        return f"<PageMetadata(key='{self.key}', value='{self.value}', page_id={self.page_id} trashed={self.trashed}>"
        

if __name__ == "__main__":
    SqlLiteHandler.download()
    SqlLiteHandler.initialize()
    Log.info("test", "I hope this works")
    page = LPage(path=__file__)
    print(page.path)
    SqlLiteHandler.upload()
