import jwt
import datetime
from .credentials import *


def getAccessToken(email):
    
    exp_time=(datetime.datetime.utcnow()+datetime.timedelta(minutes=10))
    init_time=datetime.datetime.utcnow()
    
    payload_data={
        "email":email,
        "iat":init_time,
        "exp":exp_time,
    }

    access_token = jwt.encode(
        payload=payload_data, key=tokens_secret, algorithm=tokens_encryption_algorithm
    ).decode("utf-8")

    return access_token, exp_time


def getRefreshToken(email):
    
    exp_time=(datetime.datetime.utcnow()+datetime.timedelta(minutes=1))
    init_time=datetime.datetime.utcnow()

    payload_data = {
        "email": email,
        "iat": init_time,
        "exp": exp_time,
    }

    refresh_token = jwt.encode(
        payload=payload_data, key=tokens_secret, algorithm=tokens_encryption_algorithm
    ).decode("utf-8")

    return refresh_token


def decodeToken(token):
    payload_data = jwt.decode(
        jwt=token, key=tokens_secret, algorithms=tokens_encryption_algorithm
    )

    return payload_data["email"]
