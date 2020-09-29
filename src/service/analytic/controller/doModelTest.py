from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class DoModelTest(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token',type=str,required=True)
        parser.add_argument('modelIndex', type=str, required=True)
        parser.add_argument('fileID', type=str, required=True)
        parser.add_argument('label', type=str)
        args = parser.parse_args()
        logging.debug(f"[DoModelTest] args: {args}")

        modelIndex = args['modelIndex']
        token = args['token']
        fileID = args['fileID']
        label = args['label']
        
        if label == None:
            label = ''

        #check user isLogin
        if tokenValidator(token):
            try:
                db=sql()
                db.cursor.execute(f"select * from model where `model_index`='{modelIndex}'")
                result = db.cursor.fetchone()
                if(result[1] != None):
                    form = {
                        'modelUid': result[1],
                        'fileUid': fileID,
                        'label': label,
                        'token': token
                    }            
                    resp = requests.post(coreApi.DoModelTest, data=form)
                    response = resp.json()
                    return response, 200
                else:
                    return {"status":"error","msg":"model id or file id not found","data":{}},500
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()
        else:
            return {"status":"error","msg":"user did not login","data":{}},401