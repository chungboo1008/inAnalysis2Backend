from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.model.service.modelService import ModelService
import logging
import requests

param=params()
coreApi=coreApis()

class DeleteModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('modelIndex', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[DeleteModel] args: {args}")

        modelIndex = args['modelIndex']
        token = args['token']

        #check user isLogin
        if tokenValidator(args['token']):
            try:
                db=sql()
                db.cursor.execute(f"select * from model where `model_index`='{modelIndex}'")
                result = db.cursor.fetchone()
                if result[1] != None:
                    status, resp = ModelService().deleteModel(result[1], token)
                    if(status):
                        return {"status":"success","msg":"","data":{}},200
                    else:
                        return resp
                else:
                    db.cursor.execute(f"delete from model where `model_index` = '{modelIndex}'")
                    db.conn.commit()
                    logging.info(f"[DeleteModel] OK with file id {modelIndex}")
                    return {"status":"success","msg":"can not find model","data":{}},200
                
            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg":f"{e}","data":{}},500

        else:
            return {"status":"error","msg":"user did not login","data":{}},401
class DeleteModelByProject():
    def delete(self, projectID, token):
        try:
            db=sql()
            db.cursor.execute(f"select model_index from model where `project_id`='{projectID}'")
            result = db.cursor.fetchall()
            modelIndexList = [a[0] for a in result]
            for modelIndex in modelIndexList:
                db.cursor.execute(f"select * from model where `model_index`='{modelIndex}'")
                result = db.cursor.fetchone()
                if(result[1] != None):
                    form = {
                        'modelUid': result[1],
                        'token': token
                    }
                    response = requests.post( coreApi.DeleteModel, data= form)
                    responseObj = response.json()
                    if responseObj["status"] == "success":
                        db.cursor.execute(f"delete from model where `model_index` = '{modelIndex}'")
                        db.conn.commit()
                    else:
                        return False
                else:
                    db.cursor.execute(f"delete from model where `model_index` = '{modelIndex}'")
                    db.conn.commit()
            return True
        except Exception as e:
            logging.error(str(e))
            db.conn.rollback()
            return False
        finally:
            db.conn.close()
