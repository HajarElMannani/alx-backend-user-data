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


class SessionAuth(Auth):
    '''creating a session authentication'''
    pass
