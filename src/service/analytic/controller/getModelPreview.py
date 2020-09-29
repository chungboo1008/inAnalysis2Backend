from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.analytic.service.analyticService import AnalyticService
import logging
import requests

param=params()
coreApi=coreApis()

class GetModelPreview(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('modelIndex', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetModelPreview] args: {args}")

        modelIndex = args['modelIndex']
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            try:
                db=sql()
                db.cursor.execute(f"select * from model where `model_index`='{modelIndex}'")
                result = db.cursor.fetchone()
                if(result[1] != None):
                    response = AnalyticService().getModelPreview(token, result[1])
                    return response, 200
                else:
                    return {"status":"error","msg":"model id not found","data":{}},500
            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg":f"{str(e)}","data":{}},500
                db.conn.rollback()
            finally:
                db.conn.close()
        else:
            return {"status":"error","msg":"user did not login","data":{}},401