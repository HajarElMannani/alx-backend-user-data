#!/usr/bin/env python3
"""
Manage the API authentication
"""
from typing import List, TypeVar
from flask import Flask, jsonify, abort, request


class Auth():
    '''class to manage the API authentication.'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' that returns False'''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith('/'):
            path = path + '/'
        if path in excluded_paths:
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
