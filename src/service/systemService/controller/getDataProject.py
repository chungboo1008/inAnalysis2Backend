from flask import make_response
from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests
import mimetypes

param=params()
coreApi = coreApis()

class GetDataProject(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type= str, required=True)
        args = parser.parse_args()
        logging.debug(f"[GetDataProject] args: {args}")

        token = args['token']
        
    #check user isLogin
        if tokenValidator(token):
            try:
                resp = requests.get( coreApi.GetDataProject)
                return resp.json()
            except Exception as e:
                logging.error(str(e))


        else:
            return {"status":"error","msg":"user did not login","data":{}},401    

