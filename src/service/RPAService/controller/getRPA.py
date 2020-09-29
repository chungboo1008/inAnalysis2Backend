from flask_restful import Resource, reqparse
from flask import make_response
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.RPAService.utils import RPAUidGenerator
import logging
import requests
import json

param=params()

class GetRPA(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()

        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            resp = []
            try:
                db=sql()
                db.cursor.execute(f"select * from RPA where `top_version` = 'Y'")
                result = db.cursor.fetchall()
                data=[list(a) for a in result]
                for item in data:
                    db=sql()
                    db.cursor.execute(f"select * from user where `user_id`='{item[0]}'")
                    result = db.cursor.fetchone()
                    respItem = {
                        'RPAID': item[3],
                        'RPADescription': item[5],
                        'RPAName': item[6],
                        'userName': result[1],
                        'projectID': item[1]
                    }
                    resp.append(respItem)
                return {"status":"success","msg":"","data":{'rpaList': resp}},200
            except Exception as e:
                logging.debug(f"[getRPA] error: {e}")
                return {"status":"error","msg":f"{e}","data":{}},200
                db.conn.rollback()
            finally:
                db.conn.close()  
        else:
            return {"status":"error","msg":"user did not login","data":{}},401