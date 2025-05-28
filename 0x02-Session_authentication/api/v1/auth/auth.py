#!/usr/bin/env python3
"""
Manage the API authentication
"""
from typing import List, TypeVar
from flask import Flask, jsonify, abort, request
from os import getenv


class Auth():
    '''class to manage the API authentication.'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' that returns False'''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith('/'):
            path = path + '/'
        for paths in excluded_paths:
            if paths.endswith('*'):
                if path.startswith(paths[:-1]):
                    return False
            else:
                if not paths.endswith('/'):
                    paths += '/'
                if path == paths:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        '''returns None'''
        if request is None:
            return None
        header_req = request.headers.get('Authorization')
        if header_req is None:
            return None
        return header_req

    def current_user(self, request=None) -> TypeVar:
        '''returns None'''
        return None

    def session_cookie(self, request=None):
        '''Method that returns a cookie value from a request'''
        if request is None:
            return None
        _my_session_id = getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
