from contextlib import contextmanager
from typing import *
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from extensions.oop.singleton import SingletonClass
import logging
from .secrets import DbSecret

# Intialize logger.
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


# sqlalchemy intialization
Base = declarative_base()


@SingletonClass(
    username = DbSecret.username,
    password = DbSecret.password,
    dbname = DbSecret.dbname,
    connection_address= DbSecret.connection_address
)
class MYSQL_DB:
    def __init__(self, 
                *, 
                username : str, 
                password : str, 
                dbname : str,
                connection_address : str
                ):

        connection_url : str = f"mysql+pymysql://{username}:{password}@{connection_address}/{dbname}"
        try:
            engine = create_engine(connection_url, echo=True)

            self.session = (sessionmaker(bind=engine))()
            self.connection = engine.connect()
        except: 
            logger.error(f"Failed to connect to Database")
            # Raises the exception.
            raise

    
    @classmethod
    @contextmanager
    def start_transaction(cls):
        """
            This method autocommit's all the transcations made on this session.
        """
        try: 
            yield cls.get_instance().session
        finally:
            cls.get_instance().session.commit()


    def close_resources(self):
        """
            Close all the db resources.
        """
        self.connection.close()
        self.session.close_all()
