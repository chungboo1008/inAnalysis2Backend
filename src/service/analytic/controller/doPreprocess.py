from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.analytic.service.analyticService import AnalyticService
import logging
import requests

param=params()
coreApi=coreApis()

class DoPreprocess(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileID', type=str, required=True)
        parser.add_argument('action', type=str, required=True)
        parser.add_argument('fileNameAfterProcessing', type=str, required=True)
        parser.add_argument('userID', type=str, required=True)
        parser.add_argument('projectID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[DoPreprocess] args: {args}")

        fileID = args['fileID']
        action = args['action']
        token = args['token']
        fileNameAfterProcessing = args['fileNameAfterProcessing']
        userID = args['userID']
        projectID = args['projectID']

        #check user isLogin
        if tokenValidator(token):
            response = AnalyticService().doPreprocess(token, fileID, action)
            
            if response["status"] == "success":
                try:
                    newFileID = response["data"]["fileUid"]
                    db=sql()
                    db.cursor.execute(f"insert into file (`file_id`,`file_name`,`user_id`,`project_id`) values ('{newFileID}','{fileNameAfterProcessing}','{userID}','{projectID}');")
                    db.conn.commit()
                    logging.info(f"[DoPreprocess] OK with file uid {newFileID}")
                    return response
                except Exception as e:
                    db.conn.rollback()
                    logging.error(str(e))
                finally:
                    db.conn.close()
                
            else:
                return response
            return response    
        else:
            return {"status":"error","msg":"user did not login","data":{}},401