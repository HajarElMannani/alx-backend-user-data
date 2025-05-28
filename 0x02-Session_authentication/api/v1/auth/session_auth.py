#!/usr/bin/env python3
"""
Manage the API authentication
"""
from typing import List, TypeVar
from flask import Flask, jsonify, abort, request
from api.v1.auth.auth import Auth
import base64
import binascii
import uuid
from models.user import User


class SessionAuth(Auth):
    '''creating a session authentication'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''Method creates a Session ID for a user_id'''
        if user_id is None or not isinstance(user_id, str):
            return None
        id = str(uuid.uuid4())
        self.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Method returns a User ID based on a Session ID'''
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''Method that returns a User instance based on a cookie value'''
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        '''Method that deletes the user session / logout'''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id ) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
