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

class AddCourse(Resource):
    def post(self):
        fName='[AddCourse]'
        parser = reqparse.RequestParser()
        parser.add_argument('courseName', type=str,required=True)
        parser.add_argument('courseYear',type=str,required=True)
        parser.add_argument('jobName',type=str,required=True)
        parser.add_argument('deadline',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        
        courseName = args['courseName']
        courseYear=args['courseYear']
        jobName=args['jobName']
        deadline=args['deadline']
        token=args['token']
        
        #check user isLogin
        if tokenValidator(token):
            args.pop('token')
            logging.debug(f"[AddCourse] args: {args}")

            #generate course UID and save
            uid=courseIndexGenerator().uid
            logging.debug(f'[AddCourse] course UID:{uid}')

            try:
                db=sql()
                db.cursor.execute(f"insert into course (`course_id`,`course_name`,`course_year`,`course_jobName`,`course_deadline`) values ('{uid}','{courseName}','{courseYear}','{jobName}','{deadline}');")
                db.conn.commit()
                return {"status":"success","msg":"","data":{"courseID":uid}},201

            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg":str(e),"data":{}},400
            finally:
                db.conn.close()
            

            

        

            
        
        else:
            return {"status":"error","msg":"user did not login","data":{}},401