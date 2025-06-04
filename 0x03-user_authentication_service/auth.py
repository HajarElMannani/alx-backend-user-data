#!/usr/bin/env python3
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    '''returns salted hash of the input
    password, hashed with bcrypt.hashpw.'''
    hashed = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """Generate uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''user registration'''
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User <{user.email}> already exists')
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email, hashed)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        hashed = user.hashed_password
        pswd = bcrypt.checkpw(password.encode('UTF-8'), hashed)
        if pswd:
            return True
        return False

    def create_session(self, email: str) -> str:
        """"Create a new user seesion"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
