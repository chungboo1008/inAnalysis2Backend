from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.analytic.service.analyticService import AnalyticService
import logging
import requests

param=params()
coreApi=coreApis()

class DoCorrelationByFile(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        parser.add_argument('correlationAlgoName', type=str, required=True)
        args = parser.parse_args()
        logging.debug(f"[DoCorrelationByFile] args: {args}")

        fileID = args['fileID']
        token = args['token']
        correlationAlgoName = args['correlationAlgoName']

        #check user isLogin
        if tokenValidator(token):
            return AnalyticService().doCorrelation(fileID, correlationAlgoName, token)
        else:
            return {"status":"error","msg":"user did not login","data":{}},401