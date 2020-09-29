from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.RPAService.utils import RPAUidGenerator, fileChecker
import requests
import glob
import logging

# app = Flask(__name__)
# api = Api(app)

param=params()
coreApi = coreApis()

class ImportRPA(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files',required=True)
        parser.add_argument('userID',type=str,required=True)
        parser.add_argument('projectID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[ImportRPA] args: {args}")
        file = args['file']
        userID=args['userID']
        projectID=args['projectID']
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            #check filetype
            filename=file.filename
            filetype=filename[filename.rfind("."):]
            logging.debug(f"[ImportRPA] File type:{filetype}")
            if filetype != '.json':
                return {"status":"error","msg":"file type error","data":{}},400
            
            uid = RPAUidGenerator().uid
            savedPath=param.RPAFilepath +'\\'+ uid + '.json'
            try:
                file.save(savedPath)
            except Exception as e:
                return {"status":"error","msg":f"file error:{e}","data":{}},400

            try:
                fileChecker(savedPath).check()
            except Exception as e:
                return {"status":"error","msg":str(e),"data":{}},400

            try:
                db=sql()
                db.cursor.execute(f"select MAX(version) from RPA where `project_id`='{projectID}'")
                result,  = db.cursor.fetchone()
                if result == None:
                    version = 1
                    
                else:
                    version = result + 1
                    db.cursor.execute(f"update RPA set `top_version`='N' where `user_id` = '{userID}' and `project_id` = '{projectID}'")
                    db.conn.commit()
                db.cursor.execute(f"insert into RPA (`user_id`,`project_id`, `version`, `RPA_id`, `top_version`, `name`, `description`) values ('{userID}','{projectID}','{version}','{uid}','Y', '', '');")
                db.conn.commit()
                return {"status":"success","msg":"","data":{"RPAID":uid}},201
            except Exception as e:
                logging.debug(f"[ImportRPA] error: {e}")
                db.conn.rollback()
                return {"status":"error","msg":"","data":{}},400
            finally:
                db.conn.close()
        else:
            return {"status":"error","msg":"user did not login","data":{}},401