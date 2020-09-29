from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator,sql
from service.courseService.utils import courseIndexGenerator, fileChecker, randomIndex
import requests
import glob
import logging

param=params()

class UploadStudentFile(Resource):
    def post(self):
        fName='[UploadStudent]'
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files',required=True)
        parser.add_argument('courseID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        
        file = args['file']
        courseID = args['courseID']
        token=args['token']
        
        #check user isLogin
        if tokenValidator(token):
            args.pop('token')
            logging.debug(f"[UploadStudent] args: {args}")
            studentFileTypeList=param.studentFileTypeList   

            # #check filetype
            filename=file.filename
            filetype=filename[filename.rfind("."):]
            logging.debug(f"[UploadStudent] File type:{filetype}")
            if filetype not in studentFileTypeList:
                return {"status":"error","msg":"file type error","data":{}},400

            # file save
            savedPath='./src/student/'+courseID+filetype

            try:
                file.save(savedPath)
            except Exception as e:
                return {"status":"error","msg":f"file error:{e}","data":{}},400

            try:
                fileChecker(savedPath, courseID).studentDataChecker()
                randomIndex(savedPath, courseID).randomIndexGenerator()
            except Exception as e:
                logging.error(f'{fName}{e}')
                return {"status":"error","msg":str(e),"data":{}},400

            return {"status":"success","msg":"upload success"},200

        

            
        
        else:
            return {"status":"error","msg":"user did not login","data":{}},401