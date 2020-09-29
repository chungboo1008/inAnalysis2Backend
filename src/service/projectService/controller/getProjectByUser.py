from flask import session
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging

param=params()

class GetProjectByUserID(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetProject] args: {args}")

        userID = args['userID']

        #check user isLogin
        if tokenValidator(args['token']):
            
            resp = []
            try:
                db=sql()
                db.cursor.execute(f"select * from project where `user_id`='{userID}'")
                result = db.cursor.fetchall()
                data=[list(a) for a in result]
                for item in data:
                    respItem = {
                        'projectID': item[0],
                        'projectName': item[2],
                        'projectType': item[3],
                        'dataType': item[4]
                    }
                    resp.append(respItem)
            except Exception as e:
                db.conn.rollback()
            finally:
                db.conn.close()
            logging.debug(f"[GetProject] resp: {resp}")
            return {"status":"success","msg":"","data":{'projectList': resp}},200


        else:
            return {"status":"error","msg":"user did not login","data":{}},401