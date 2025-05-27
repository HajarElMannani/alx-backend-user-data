#!/usr/bin/env python3
"""
Manage the API authentication
"""
from typing import List, TypeVar
from flask import Flask, jsonify, abort, request
from api.v1.auth.auth import Auth


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
