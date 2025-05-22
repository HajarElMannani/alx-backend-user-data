#!/usr/bin/env python3
'''Function hash_password'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''Function to encrypt passwords'''
    hashed = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' validate that the provided password matches the hashed password'''
    if bcrypt.checkpw(password.encode('UTF_8'), hashed_password):
        return True
    else:
        return False
