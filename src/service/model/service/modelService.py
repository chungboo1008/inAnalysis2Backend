from flask_restful import Resource, reqparse
from params import params 
#import params as params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.model.utils import modelIndexGenerator
import requests
import glob
import logging

param=params()
coreApi=coreApis()

class ModelService:
    def addModel(self, projectID, fileID, modelName, userID, token):
        index = modelIndexGenerator().index
        try:
            db=sql()
            db.cursor.execute(f"insert into model (`model_index`,`user_id`,`project_id`,`file_id`,`model_name`) values ('{index}','{userID}','{projectID}','{fileID}','{modelName}');")
            db.conn.commit()
            return {"status":"success","msg":"","data":{"modelID":index}},201

        except Exception as e:
            return {"status":"error","msg":str(e),"data":{}},400
        finally:
            db.conn.close()

    def getModelStatus(self, token, modelUid):
        try:
            form = {
                "token": token,
                "modelUid": modelUid
            }
            resp = requests.get( coreApi.GetModelStatus, data= form)
            response = resp.json()
            return response
        except Exception as e:
            return {"status":"error","msg":f"{e}","data":{}},500


    def deleteModel(self, modelIndex, token):
        try:
            logging.debug(f'[DeleteModel]: {modelIndex}')
            db=sql()
            form = {
                'modelUid': modelIndex,
                'token': token
            }
            response = requests.post( coreApi.DeleteModel, data= form)
            responseObj = response.json()
            logging.error(f'[deleteModel]: {responseObj}')
            if responseObj["status"] == "success":
                logging.info('success')
                db.cursor.execute(f"delete from model where `model_id` = '{modelIndex}'")
                db.conn.commit()
                logging.info(f"[DeleteModel] OK with model id {modelIndex}")
                return (True, responseObj)
            else:
                return (False, responseObj)

            
        except Exception as e:
            logging.error(str(e))
            db.conn.rollback()
            return (False, {"status":"error","msg":"","data":{}},500)
        finally:
            db.conn.close()

    def getModelByProject(self, projectID, token):
        logging.debug(f'[getModelByProject], {projectID}, {token}')
        respList = []
        try:
            db=sql()
            db.cursor.execute(f"select * from model where `project_id`='{projectID}'")
            result = db.cursor.fetchall()
            data=[list(a) for a in result]
            for item in data:
                if item[1] == None or item[1]=="None":
                    respItem = {
                        'modelIndex': item[0],
                        'fileID': item[4],
                        'modelName': item[5],
                        'algoName': item[6]
                    }
                    respList.append(respItem)
                else:
                    form = {
                        "token": token,
                        "modelUid": item[1]
                    }
                    resp = requests.get( coreApi.GetModelStatus, data= form)
                    response = resp.json()
                    if(response['status'] == 'success'):
                        if(response['data'] != 'fail'):
                            respItem = {
                                'modelIndex': item[0],
                                'status': response['data'],
                                'fileID': item[4],
                                'modelName': item[5],
                                'algoName': item[6]
                            }
                        else:
                            resp = requests.get( coreApi.GetModelFailReason, data= form)
                            failReason = resp.json()
                            if(response['status'] == 'success'):
                                respItem = {
                                    'modelIndex': item[0],
                                    'status': response['data'],
                                    'fileID': item[4],
                                    'modelName': item[5],
                                    'algoName': item[6],
                                    'failReason': failReason['data']
                                }
                        respList.append(respItem)
                    else:
                        return {"status":"fail","msg":"get model status error","data":{}},500
        except Exception as e:
            logging.error(str(e))
            db.conn.rollback()
        finally:
            db.conn.close()
        logging.debug(f"[GetModel] resp: {respList}")
        return {"status":"success","msg":"","data":{'modelList': respList}},200


