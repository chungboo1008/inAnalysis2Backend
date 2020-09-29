from service.userService.utils import userSignupToken
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

class SingupVerify(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str,required=True)
        args = parser.parse_args()
        logging.info(f'[SingupVerify] {args}')

        try:
            data= userSignupToken().userSignupTokenValidator(args['token'])
            logging.info(data)
            if data != False:
                db=sql()
                db.cursor.execute(f"insert into user (`user_id`,`user_name`,`user_account`,`user_email`,`user_password`,`user_roles`) values ('{data['sub']}','{data['username']}','{data['account']}','{data['email']}','{data['password']}', 1);")
                db.conn.commit()
                return {"status":"success","msg":"","data":{"user":data['sub']}},201
            else:
                return {"status":"error","msg":"verify error","data":{}},400
        except Exception as e:
            logging.error(f'[Signup Verify] {e}')
            return {"status":"error","msg":f"{e}","data":{}},400
            db.conn.rollback()
        finally:
            db.conn.close()

