from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.analytic.service.analyticService import AnalyticService
import logging
import requests

param=params()
coreApi=coreApis()

class DoCorrelation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('modelIndex', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        parser.add_argument('correlationAlgoName', type=str, required=True)
        args = parser.parse_args()
        logging.debug(f"[DoCorrelation] args: {args}")

        modelIndex = args['modelIndex']
        token = args['token']
        correlationAlgoName = args['correlationAlgoName']

        #check user isLogin
        if tokenValidator(token):
            try:
                db=sql()
                db.cursor.execute(f"select * from model where `model_index`='{modelIndex}'")
                result = db.cursor.fetchone()
                if(result[4] != None):
                    return AnalyticService().doCorrelation(result[4], correlationAlgoName, token)
                else:
                    return {"status":"error","msg":"file id not found","data":{}},500
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()
        else:
            return {"status":"error","msg":"user did not login","data":{}},401