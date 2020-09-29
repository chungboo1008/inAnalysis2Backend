from flask import session
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging

param=params()

class GetUserInfo(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetUserInfo] args: {args}")

        token = args['token']
        userID = args['userID']

        #check user isLogin
        if tokenValidator(token):
            try:
                db=sql()
                db.cursor.execute(f"select (select count(*) from project where `user_id`='{userID}') as projectSum,(select count(*) from file where `user_id`='{userID}') as fileSum,(select count(*) from model where `user_id`='{userID}') as modelSum ")
                result = db.cursor.fetchone()
                return {"status":"success","msg":"","data":{'projectSum': result[0], 'fileSum': result[1], 'modelSum': result[2]}},200
            except Exception as e:
                logging.info(e)
                db.conn.rollback()
            finally:
                db.conn.close()
            # return {"status":"success","msg":"","data":{'projectList': resp}},200


        else:
            return {"status":"error","msg":"user did not login","data":{}},401