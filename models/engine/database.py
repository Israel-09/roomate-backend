#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.profile import Profile
from models.preference import Preference
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from os import getenv
from models.base_model import Base

class DB:
    """
    database class
    """
    def __init__(self):
        """initialize database"""
        MYSQL_USER = getenv('MYSQL_USER')
        MYSQL_PWD = getenv('MYSQL_PWD')
        MYSQL_HOST = getenv('MYSQL_HOST')
        MYSQL_DB = getenv('MYSQL_DB')
        ENV = getenv('ENV')
        url = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB)
        print(url)
        self._engine = create_engine(url)
        Base.metadata.create_all(self._engine)
        self.__session = None
    
    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str):
        """adds a new user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user 

    def find_user_by(self, **kwargs):
        """find user by a parameter"""
        if not kwargs:
            raise InvalidRequestError

        session = self._session
        user = session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound('No result  found')
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update a user field
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
        return None
    
    def all_user_preference(self):
        """returns all the columns in the preference table"""
        preferences = self._session.query(Preference).all()
        return preferences

    def add(self, obj):
        """add a new object to the database"""
        self.__session.add(obj)
        self.__session.commit()

    def save(self):
        """commit a new change to the database"""
        self.__session.commit()
