#-*- coding: utf-8 -*-
import os
import sys
import json
import logging

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from ..utils.common import Singleton

log = logging.getLogger("qi.database")

class Database(object):
    __metaclass__ = Singleton

    def __init__(self, Base, engine):
        self.Base = Base
        self.engine = engine
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)        

    def __del__(self):
        """Disconnects pool."""
        self.engine.dispose()

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            log.error("Database Error. %s", e)
            session.rollback()
        finally:
            session.close()

    def create_all(self):
        """ creates all tables. """
        try:
            self.Base.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            log.error("Unable to create or connect to database: %s", e)

    def drop_all(self):
        """Drop all tables."""
        try:
            self.Base.metadata.drop_all(self.engine)
        except SQLAlchemyError as e:
            log.error("Unable to drop all tables of the database: %s", e)
