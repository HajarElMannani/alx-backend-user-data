#!/usr/bin/env python3
"""
Manage the API authentication
"""
from typing import List, TypeVar
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


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