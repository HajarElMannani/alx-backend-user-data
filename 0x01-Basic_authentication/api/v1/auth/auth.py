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
        return False

    def authorization_header(self, request=None) -> str:
        '''returns None'''
        return None

    def current_user(self, request=None) -> TypeVar:
        '''returns None'''
        return None
