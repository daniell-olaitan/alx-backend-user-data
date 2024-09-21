#!/usr/bin/env python3
"""
Module for Database Implementation
"""
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import typing as t

from user import Base
from user import User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user to users table in the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: t.Mapping) -> User:
        """
        Get a user using attributes
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()

            return user
        except NoResultFound:
            raise
        except Exception:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs: t.Mapping) -> None:
        """
        Update a given user
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in User.__table__.columns.keys():
                raise ValueError

            setattr(user, key, value)

        self._session.add(user)
        self._session.commit()
