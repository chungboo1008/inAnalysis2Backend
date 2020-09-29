from params import params
import glob
import uuid
import logging
import time
import jwt
from utils import sql

param = params()
class userUidGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        while self.checkUserID(self.uid) != ():
            self.uid=str(uuid.uuid1())

    def checkUserID(self, userUid):
        db=sql()
        db.cursor.execute(f"select * from user where `user_id`='{self.uid}'")
        return db.cursor.fetchall()

class userSignupToken():
    def userSignupTokenGenerator(self,data, key = param.secretKey, expire=360):
        try:
            payload = {
                "iss": "inanalysis.com",
                "iat": int(time.time()),
                "exp": int(time.time()) + expire,
                "aud": "www.inanalysis.com",
                "sub": data['userID'],
                "account": data['account'],
                "username": data['userName'],
                "password": data['password'],
                "email": data['email']
            }
            token = jwt.encode(payload, key, algorithm='HS256').decode('utf-8')
            return token
        except Exception as e:
            return (False, e)

    def userSignupTokenValidator(self, token, key = param.secretKey):
        try :
            payload = jwt.decode(token, key, audience='www.inanalysis.com', algorithms=['HS256'])
            if payload:
                return payload
            return False
        except Exception as e:
            return False

class userPasswordToken():
    def userPasswordTokenGenerator(self,data, key = param.secretKey, expire=360):
        try:
            payload = {
                "iss": "inanalysis.com",
                "iat": int(time.time()),
                "exp": int(time.time()) + expire,
                "aud": "www.inanalysis.com",
                "sub": data['userID'],
                "account": data['account']
            }
            token = jwt.encode(payload, key, algorithm='HS256').decode('utf-8')
            return token
        except Exception as e:
            return (False, e)

    def userPasswordTokenValidator(self, token, key = param.secretKey):
        try :
            payload = jwt.decode(token, key, audience='www.inanalysis.com', algorithms=['HS256'])
            if payload:
                return payload
            return False
        except Exception as e:
            return False
