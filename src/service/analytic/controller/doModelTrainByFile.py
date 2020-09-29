from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests
from service.analytic.service.analyticService import AnalyticService

param=params()
coreApi=coreApis()

class DoModelTrainByFile(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('FileIndex', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        parser.add_argument('dataType', type=str, required=True)
        parser.add_argument('projectType', type=str, required=True)
        parser.add_argument('algoName', type=str, required=True)
        parser.add_argument('param', type=str, required=True)
        parser.add_argument('input', type=str, required=True)
        parser.add_argument('output', type=str, required=True)
        args = parser.parse_args()
        logging.debug(f"[DoModelTrain] args: {args}")

        fileIndex = args['FileIndex']
        token = args['token']
        dataType = args['dataType']
        projectType = args['projectType']
        algoName = args['algoName']
        param = args['param']
        inputColumn = args['input']
        output = args['output']

        #check user isLogin
        if tokenValidator(token):
            try:
                     
                response = AnalyticService().trainModel(token, fileIndex, dataType, projectType, algoName, param, inputColumn, output)
                if response['status'] == 'success':
                    try:
                        return response, 200
                    except Exception as e:
                        logging.error(str(e))
                else: 
                    return {"status":"error","msg":response['msg'],"data":{}},500
            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg":f"{str(e)}","data":{}},500
            
        else:
            return {"status":"error","msg":"user did not login","data":{}},401