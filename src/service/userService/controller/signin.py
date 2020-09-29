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

class Singin(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('account', type=str,required=True)
            parser.add_argument('password',type=str,required=True)
            # parser.add_argument('user',type=str,required=True)
            args = parser.parse_args()

            md5 = hashlib.md5()
            md5.update(args['password'].encode("utf-8"))

            password = md5.hexdigest()
            try:
                db=sql()
                db.cursor.execute(f"select * from user where `user_account`='{args['account']}' AND `user_password`='{password}'")
                result = db.cursor.fetchone()

                try:
                    if result != None :
                        data = {
                            'userID' : result[0],
                            'userName' : result[1]
                        }
                        token = tokenGenerator(data)
                        return {"status": "success","msg":"","data": {"userID":f'{result[0]}',"userName":f'{result[1]}','userRole' :f'{result[5]}', "token":f'{token}'}}
                    else:
                        return {"status":"error","msg":"user don't exist"},400
                except Exception as e:
                    logging.info(str(e))

            except Exception as e:
                db.conn.rollback()
            finally:
                db.conn.close()

        except Exception as e:
            return {"status":"error","msg":f"login error:{e}","data":{}},400