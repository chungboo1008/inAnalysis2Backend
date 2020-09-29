from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.file.service.fileService import FileService
import logging
import requests

param=params()
coreApi=coreApis()

class DeleteFile(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[DeleteFile] args: {args}")

        fileID = args['fileID']
        token = args['token']

        #check user isLogin
        if tokenValidator(args['token']):
            try:
                db=sql()
                responseObj = FileService().deleteFile(token, fileID)
                if responseObj["status"] == "success":
                    logging.info('success')
                    db.cursor.execute(f"delete from file where `file_id` = '{fileID}'")
                    db.conn.commit()
                    logging.info(f"[DeleteFile] OK with file id {fileID}")
                    return {"status":"success","msg":"","data":{}},200
                else:
                    return responseObj
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()


        else:
            return {"status":"error","msg":"user did not login","data":{}},401