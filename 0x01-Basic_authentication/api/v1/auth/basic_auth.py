#!/usr/bin/env python3
"""
Manage the API authentication
"""
from typing import List, TypeVar
from flask import Flask, jsonify, abort, request
from api.v1.auth.auth import Auth
import base64
import binascii
from models.user import User


class BasicAuth(Auth):
    '''Empty class'''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''Method that returns the Base64 part
          of the Authorization header for a Basic Authentication'''
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''Method that returns the decoded value
        of a Base64 string base64_authorization_header'''
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header,
                                       validate=True)
            return decoded.decode('UTF-8')
        except(binascii.Error):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''Method that returns the user email and
        password from the Base64 decoded value.'''
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''Method that returns the User instance based
        on his email and password'''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user_inst = User.search({'email': user_email})
        except Exception:
            return None
        if user_inst is None or user_inst == []:
            return None
        if user_inst[0].is_valid_password(user_pwd) is False:
            return None
        return user_inst[0]
    
    def current_user(self, request=None) -> TypeVar('User'):
        '''that overloads Auth and retrieves the User instance for a request'''
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None
        decoded_auth = self.decode_base64_authorization_header(base64_header)
        if decoded_auth is None:
            return None
        email, password = self.extract_user_credentials(decoded_auth)
        if email is None or password is None:
            return None
        user = self.user_object_from_credentials(email, password)
        if user is None:
            return None
        return user
