#!/usr/bin/env python3
"""main module to start the app"""
import requests


def register_user(email: str, password: str) -> None:
    """register the user"""
    resp = requests.post("http://0.0.0.0:5000/users",
                         data={"email": email,
                               "password": password})
    assert resp.status_code == 200 or resp.status_code == 400
    if resp.status_code == 200:
        assert resp.json() == {"email": email, "message": "user registered"}
    elif resp.status_code == 400:
        assert resp.json() == {"message": "user already registered"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
