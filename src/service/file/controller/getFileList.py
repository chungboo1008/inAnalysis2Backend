from flask import session
from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import requests
import logging
import json

param=params()
coreApi = coreApis()

class GetFileList(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetFileList] args: {args}")

        projectID = args['projectID']
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            
            resp = []
            try:
                db=sql()
                db.cursor.execute(f"select * from file where `project_id`='{projectID}'")
                result = db.cursor.fetchall()
                data=[list(a) for a in result]
                for item in data:
                    form = {
                        'fileUids': json.dumps([item[0]]),
                        'token': token
                    }
                    logging.info(f'form:{form}')
                    response = requests.post( coreApi.GetFileStatus , data= form)
                    responseObj = response.json()
                    if responseObj["status"] == 'success':
                        respItem = {
                            'fileID': item[0],
                            'fileName': item[1][:(item[1].rfind("."))],
                            'fileType': item[1][(item[1].rfind(".")+1):],
                            'fileStatus': responseObj["data"]["status"][0]
                        }
                        db.cursor.execute(f"select Count(*) from model where `file_id`='{item[0]}'")
                        result = db.cursor.fetchall()
                        if result[0][0] > 0:
                            respItem['fileStatus'] = 1
                        resp.append(respItem)
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()
            logging.debug(f"[GetFileList] resp: {resp}")
            return {"status":"success","msg":"","data":{'fileList': resp}},200


        else:
            return {"status":"error","msg":"user did not login","data":{}},401