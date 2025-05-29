#!/usr/bin/env python3
"""
Manage the API authentication
"""
from typing import List, TypeVar
from flask import Flask, jsonify, abort, request
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''class to  add an expiration date to a Session ID'''
    def __init__(self):
        '''instantiation'''
        duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''Ceate a session'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''return user_id'''
        if session_id is None:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if session is None:
            return None
        if self.session_duration <= 0:
            return session.get('user_id')
        if 'created_at' not in session:
            return None
        created = session.get('created_at')
        if created + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return session.get('user_id')
