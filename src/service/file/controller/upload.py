from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import requests
import glob
import logging

# app = Flask(__name__)
# api = Api(app)

param=params()
coreApi = coreApis()

class Upload(Resource):
    def post(self):
        fName='[Upload]'
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files',required=True)
        parser.add_argument('type',type=str,required=True)
        parser.add_argument('userID',type=str,required=True)
        parser.add_argument('projectID',type=str,required=True)
        parser.add_argument('isRPA',type=str,required=False)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[Upload] args: {args}")
        file = args['file']
        dataType=args['type']
        userID=args['userID']
        projectID=args['projectID']
        token = args['token']
        isRPA = True if (args['isRPA'] == 'Y') else False

        #check user isLogin
        if tokenValidator(token):

            pft=param.dataFileTypeList
            #check project type
            if dataType not in pft:
                return {"status":"error","msg":"project type not supported","data":{}},400
            
            #check filetype
            
            filename=file.filename
            filetype=filename[filename.rfind("."):]
            logging.debug(f"[Upload] File type:{filetype}")
            if filetype not in pft[dataType]:
                return {"status":"error","msg":"file type error","data":{}},400

            files = {
                'file': (file.filename, file.stream.read(), file.mimetype)
            }
            data = {
                'type': dataType,
                'token': token
            }

            logging.debug(f'data: {data}')
            #todo change ip
            resp = requests.post( coreApi.Upload , files = files, data= data)
            response = resp.json()
            logging.info(f'{response}')
            
            if response["status"] == "success":
                try:
                    fileID = response["data"]["fileUid"]
                    if(not isRPA):
                        db=sql()
                        db.cursor.execute(f"insert into file (`file_id`,`file_name`,`user_id`,`project_id`, `is_upload`) values ('{fileID}','{filename}','{userID}','{projectID}', '1');")
                        db.conn.commit()
                    logging.info(f"[Upload] OK with file uid {fileID}")
                    return response
                except Exception as e:
                    db.conn.rollback()
                    logging.error(str(e))
                finally:
                    db.conn.close()
                
            else:
                return response
        
        else:
            return {"status":"error","msg":"user did not login","data":{}},401