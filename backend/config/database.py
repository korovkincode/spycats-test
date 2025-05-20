from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


class Database:
    __DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(__DATABASE_URL)
    session = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    Base = declarative_base()


    @classmethod
    def setup(cls):
        cls.Base.metadata.create_all(bind=cls.engine)


    @classmethod
    def getDriver(cls):
        return cls.session()