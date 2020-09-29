from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator,sql
from service.courseService.utils import courseIndexGenerator
import requests
import glob
import logging

param=params()

class ModifyCourse(Resource):
    def post(self):
        fName='[ModifyCourse]'
        parser = reqparse.RequestParser()
        parser.add_argument('courseID', type=str,required=True)
        parser.add_argument('courseName', type=str,required=True)
        parser.add_argument('courseYear',type=str,required=True)
        parser.add_argument('jobName',type=str,required=True)
        parser.add_argument('deadline',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        
        courseID = args['courseID']
        courseName = args['courseName']
        courseYear=args['courseYear']
        jobName=args['jobName']
        deadline=args['deadline']
        token=args['token']
        
        #check user isLogin
        if tokenValidator(token):
            args.pop('token')
            logging.debug(f"[ModifyCourse] args: {args}")

            try:
                db=sql()
                db.cursor.execute(f"update course set `course_name`='{courseName}', `course_year`='{courseYear}', `course_jobName`='{jobName}', `course_deadline`='{deadline}' where `course_id`='{courseID}'")
                db.conn.commit()
                return {"status":"success","msg":"","data":{"courseID":courseID}},200

            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg":str(e),"data":{}},400
            finally:
                db.conn.close()
     
        else:
            return {"status":"error","msg":"user did not login","data":{}},401