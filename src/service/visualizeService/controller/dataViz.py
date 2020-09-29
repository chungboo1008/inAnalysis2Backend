from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class dataViz(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileID', type=str, required=True)
        parser.add_argument('algoName', type=str, required=True)
        parser.add_argument('dataCol', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[dataViz] args: {args}")

        fileID = args['fileID']
        algoName = args['algoName']
        dataCol = args['dataCol']
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            form = {
                'fileUid': fileID,
                'algoname': algoName,
                'datacol': dataCol,
                'token': token
            }
            resp = requests.post(coreApi.DoDataViz, data=form)
            response = resp.json()
            return response    
        else:
            return {"status":"error","msg":"user did not login","data":{}},401