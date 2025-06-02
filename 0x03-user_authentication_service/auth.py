#!/usr/bin/env python3
import bcrypt


def _hash_password(password: str) -> bytes:
    '''returns salted hash of the input 
    password, hashed with bcrypt.hashpw.'''
    hashed = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    return hashed