from service.userService.utils import userPasswordToken
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

class ForgetPasswordVerify(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('token', type=str,required=True)
        args = parser.parse_args()
        logging.info(f'[ForgetPasswordVerify] {args}')

        md5 = hashlib.md5()
        md5.update(args['password'].encode("utf-8"))
        password = md5.hexdigest()

        try:
            data= userPasswordToken().userPasswordTokenValidator(args['token'])
            logging.info(data)
            if data != False:
                db=sql()
                db.cursor.execute(f"update user set `user_password`='{password}' where `user_id`='{data['sub']}'")
                db.conn.commit()
                return {"status":"success","msg":"","data":{"user":data['sub']}},200
            else:
                return {"status":"error","msg":"verify error","data":{}},400
        except Exception as e:
            logging.error(f'[ForgetPasswordVerify] {e}')
            return {"status":"error","msg":f"{e}","data":{}},400
            db.conn.rollback()
        finally:
            db.conn.close()

