#!/usr/bin/env python3
'''Function hash_password'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''Function to encrypt passwords'''
    hashed = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    return hashed
