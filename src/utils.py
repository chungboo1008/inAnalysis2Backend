import logging
from params import params
import pymysql
import time
import jwt  
import json

param = params()

def tokenGenerator(data, key = param.secretKey, expire=1800):
    payload = {
        "iss": "inanalysis.com",
        "iat": int(time.time()),
        "exp": int(time.time()) + expire,
        "aud": "www.inanalysis.com",
        "sub": data['userID'],
        "username": data['userName']
    }
    logging.info(f'data: {payload}')
    token = jwt.encode(payload, key, algorithm='HS256').decode('utf-8')
    logging.info(f'token: {token}')
    return token

def tokenValidator(token, key = param.secretKey):
    try :
        payload = jwt.decode(token, key, audience='www.inanalysis.com', algorithms=['HS256'])
        if payload:
            return True
        return False
    except Exception as e:
        return False

class sql():
    def __init__(self):
        param=params()
        self.conn=pymysql.connect(param.dbhost,param.dbuser,param.dbpwd,param.dbschema)
        self.cursor=self.conn.cursor()
