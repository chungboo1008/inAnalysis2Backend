from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests
import os

param=params()
coreApi=coreApis()

class DeleteCourse(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courseID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[DeleteCourse] args: {args}")

        courseID = args['courseID']
        token = args['token']

        #check user isLogin
        if tokenValidator(args['token']):
            try:
                db=sql()
                logging.info('success')
                db.cursor.execute(f"delete from course where `course_id` = '{courseID}'")
                db.cursor.execute(f"delete from score where `course_id` = '{courseID}'")
                db.conn.commit()
                filepath = './src/student/'+courseID+'.csv'
                if os.path.isfile(filepath):
                    os.remove(filepath)
                logging.info(f"[DeleteCourse] OK with course id {courseID}")
                return {"status":"success","msg":"","data":{}},200
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()


        else:
            return {"status":"error","msg":"user did not login","data":{}},401