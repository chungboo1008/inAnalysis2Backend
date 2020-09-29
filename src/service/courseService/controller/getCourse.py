from flask import session
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging

param=params()

class GetCourse(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetCourse] args: {args}")

        #check user isLogin
        if tokenValidator(args['token']):
            
            resp = []
            try:
                db=sql()
                db.cursor.execute(f"select * from course")
                result = db.cursor.fetchall()
                data=[list(a) for a in result]
                for item in data:
                    respItem = {
                        'courseID': item[0],
                        'courseName': item[1],
                        'courseYear': item[2],
                        'jobName': item[3],
                        'deadline': item[4]
                    }
                    resp.append(respItem)
            except Exception as e:
                db.conn.rollback()
            finally:
                db.conn.close()
            logging.debug(f"[GetCourse] resp: {resp}")
            return {"status":"success","msg":"","data":{'courseList': resp}},200


        else:
            return {"status":"error","msg":"user did not login","data":{}},401