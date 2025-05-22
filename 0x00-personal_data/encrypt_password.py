#!/usr/bin/env python3
'''Function hash_password'''
import bcrypt


def hash_password(password: str) -> bytes:
    hashed = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    return hashed
