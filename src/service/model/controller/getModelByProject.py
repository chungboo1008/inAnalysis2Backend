from flask import session
from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.model.service.modelService import ModelService
import logging
import requests

param=params()
coreApi=coreApis()

class GetModelByProjectID(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetModel] args: {args}")

        projectID = args['projectID']
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            return ModelService().getModelByProject(projectID, token)
            
        else:
            return {"status":"error","msg":"user did not login","data":{}},401