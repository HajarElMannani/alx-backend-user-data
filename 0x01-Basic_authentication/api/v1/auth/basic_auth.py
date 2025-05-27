#!/usr/bin/env python3
"""
Manage the API authentication
"""
from typing import List, TypeVar
from flask import Flask, jsonify, abort, request
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''Empty class'''
    pass
