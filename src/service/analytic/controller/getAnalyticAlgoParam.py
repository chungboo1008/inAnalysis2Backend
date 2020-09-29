from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class GetAnalyticAlgoParam(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dataType',type=str,required=True)
        parser.add_argument('projectType',type=str,required=True)
        parser.add_argument('algoName',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetAnalyticAlgoParam] args: {args}")
        dataType = args['dataType']
        projectType = args['projectType']
        algoName = args['algoName']
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            form = {
                'dataType': dataType,
                'projectType':projectType,
                'algoName': algoName
            }
            resp = requests.get(coreApi.GetAnalyticAlgoParam, data=form)
            response = resp.json()
            if response['status'] == 'success':
                return resp.json(), 200
            else:
                return resp.json(), 500
        else:
            return {"status":"error","msg":"user did not login","data":{}},401