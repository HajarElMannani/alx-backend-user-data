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
