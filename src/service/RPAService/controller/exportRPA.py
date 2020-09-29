from flask_restful import Resource, reqparse
from flask import make_response
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.RPAService.utils import RPAUidGenerator
import logging
import requests
import json

param=params()

class ExportRPA(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userID', type=str, required=True)
        parser.add_argument('projectID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args() 
        # logging.debug(f"[exportRPA] args: {args}")

        userID = args['userID']
        projectID = args['projectID']
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            try:
                db=sql()
                db.cursor.execute(f"select RPA_id from RPA where `project_id`='{projectID}' and `user_id` = '{userID}' and `top_version` = 'Y'")
                result,  = db.cursor.fetchone()
                logging.debug(f"[exportRPA] result: {result}")
                with open(param.RPAFilepath + '\\'+ result + '.json') as json_file:
                    data = json_file.read()
                headers={}
                headers['Content-Type']='application/octet-stream'
                return make_response(data,200,headers)
            except Exception as e:
                logging.debug(f"[exportRPA] error: {e}")
                return {"status":"error","msg":"No version","data":{}},200
                db.conn.rollback()
            finally:
                db.conn.close()  
        else:
            return {"status":"error","msg":"user did not login","data":{}},401