from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.model.service.modelService import ModelService
import logging
import requests

param=params()
coreApi=coreApis()

class DeleteModelUID(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('modelUID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[DeleteModel] args: {args}")

        modelUID = args['modelUID']
        token = args['token']

        #check user isLogin
        if tokenValidator(args['token']):
            try:
                status, resp = ModelService().deleteModel(modelUID, token)
                if(status):
                    return {"status":"success","msg":"","data":{}},200
                else:
                    return resp
                
            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg":f"{e}","data":{}},500

        else:
            return {"status":"error","msg":"user did not login","data":{}},401
