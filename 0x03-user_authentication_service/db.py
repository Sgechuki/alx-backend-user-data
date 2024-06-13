#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import Dict


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
        Insert user
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """
        takes in arbitrary keyword arguments and
        returns the first row found in the users table
        as filtered by the method’s input arguments
        """
        key, value = [], []
        for k, v in kwargs.items():
            if hasattr(User, k):
                key.append(getattr(User, k))
                value.append(v)
            else:
                raise InvalidRequestError()
        user = self._session.query(User).filter(
                tuple_(*key).in_([tuple(value)])).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs: Dict[str, str]) -> None:
        """
        updates user
        """
        user = self.find_user_by(id=user_id)
        if user:
            for k, v in kwargs.items():
                if hasattr(user, k):
                    #attr = getattr(user, k)
                    setattr(user, k, v)
                else:
                    raise ValueError
            self._session.commit()
        return None
