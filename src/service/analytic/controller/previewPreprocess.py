from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class PreviewPreprocess(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileID', type=str, required=True)
        parser.add_argument('action', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[PreviewPreprocess] args: {args}")

        fileID = args['fileID']
        action = args['action']
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            form = {
                'fileUid': fileID,
                'action': action,
                'token': token
            }
            resp = requests.post(coreApi.PreviewPreprocess, data=form)
            response = resp.json()
            
            return response     
        else:
            return {"status":"error","msg":"user did not login","data":{}},401