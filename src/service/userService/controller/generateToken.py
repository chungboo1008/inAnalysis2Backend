from flask import session, make_response
from flask_restful import Resource, reqparse
from params import params
from utils import tokenGenerator,tokenValidator,sql
import hashlib
import glob
import uuid
import logging
import json

param=params()

class GenerateToken(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('userID', type=str,required=True)
            parser.add_argument('userName',type=str,required=True)
            args = parser.parse_args()

            userID = args['userID']
            userName = args['userName']

            try:
                data = {
                    'userID' : userID,
                    'userName' : userName
                }
                token = tokenGenerator(data)
                return {"status": "success","msg":"","data": {"userID":f'{userID}',"userName":f'{userName}', "token":f'{token}'}}
            except Exception as e:
                logging.info(str(e))

           

        except Exception as e:
            return {"status":"error","msg":f"login error:{e}","data":{}},400