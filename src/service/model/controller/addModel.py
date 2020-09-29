from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
from service.model.service.modelService import ModelService
import glob
import logging

param=params()

class AddModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectID', type=str,required=True)
        parser.add_argument('userID', type=str,required=True)
        parser.add_argument('fileID', type=str,required=True)
        parser.add_argument('modelName',type=str,required=True)
        parser.add_argument('token',type=str,required=False)
        args = parser.parse_args()
        logging.info(f'[AddModel] {args}')


        projectID = args['projectID']
        fileID = args['fileID']
        modelName = args['modelName']
        userID = args['userID']
        token = args['token']
        
        #check user isLogin
        if tokenValidator(token):
            return ModelService().addModel(projectID, fileID, modelName, userID, token)

        else:
            return {"status":"error","msg":"user did not login","data":{}},401    

