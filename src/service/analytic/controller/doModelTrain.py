from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests
from service.analytic.service.analyticService import AnalyticService
from service.model.service.modelService import ModelService

param=params()
coreApi=coreApis()

class DoModelTrain(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('modelIndex', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        parser.add_argument('dataType', type=str, required=True)
        parser.add_argument('projectType', type=str, required=True)
        parser.add_argument('algoName', type=str, required=True)
        parser.add_argument('param', type=str, required=True)
        parser.add_argument('input', type=str, required=True)
        parser.add_argument('output', type=str, required=True)
        args = parser.parse_args()
        logging.debug(f"[DoModelTrain] args: {args}")

        modelIndex = args['modelIndex']
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
                db=sql()
                db.cursor.execute(f"select * from model where `model_index`='{modelIndex}'")
                result = db.cursor.fetchone()
                if result[4] != None:
                    if(result[1] != None):
                        form = {
                            'modelUid': result[1],
                            'token': token
                        }
                        response = requests.post( coreApi.DeleteModel, data= form)
                        responseObj = response.json()
                        logging.info(f'[deleteModel]: {responseObj}')
                        if responseObj["status"] == "success":
                            db.cursor.execute(f"update model set `model_id`='{None}' where `model_id` = '{modelIndex}'")
                            db.conn.commit()
                            logging.info(f"[updateModel] OK with model id {modelIndex}")

                    response = AnalyticService().doModelTrain(token, result[4], dataType, projectType, algoName, param, inputColumn, output)
                    logging.debug(f"[DoModelTrain] response: {response}")
                    if response['status'] == 'success':
                        try:
                            db=sql()
                            db.cursor.execute(f"update model set `model_id`='{response['data']['modelUid']}', `algo_name`='{algoName}' where `model_index`='{modelIndex}'")
                            db.conn.commit()
                            return response, 200
                        except Exception as e:
                            logging.error(str(e))
                            db.conn.rollback()
                    else: 
                        return {"status":"error","msg":response['msg'],"data":{}},500
                else:
                    return {"status":"error","msg":"file id not found","data":{}},500
            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg":f"{str(e)}","data":{}},500
                db.conn.rollback()
            finally:
                db.conn.close()
            
        else:
            return {"status":"error","msg":"user did not login","data":{}},401