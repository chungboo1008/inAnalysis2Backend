from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class DoModelPredict(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        parser.add_argument('modelIndex', type=str, required=True)
        parser.add_argument('preprocessFileName', type=str, required=True)
        parser.add_argument('predictFileName', type=str, required=True)
        parser.add_argument('preprocess', type=str, required=True)
        parser.add_argument('projectID', type=str, required=True)
        parser.add_argument('userID', type=str, required=True)
        args = parser.parse_args()
        logging.debug(f"[DoModelPredict] args: {args}")

        fileID = args['fileID']
        modelIndex = args['modelIndex']
        preprocessFileName = args['preprocessFileName']
        predictFileName = args['predictFileName']
        token = args['token']
        preprocess = args['preprocess']
        projectID = args['projectID']
        userID = args['userID']

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
                        'preprocess': preprocess,
                        'token': token
                    }            
                    resp = requests.post(coreApi.DoModelPredict, data=form)
                    response = resp.json()
                    try:
                        db.cursor.execute(f"select * from file where `file_id`='{result[4]}'")
                        fileObject = db.cursor.fetchone()
                        fileType = fileObject[1][(fileObject[1].rfind(".")+1):]
                        logging.info(f'{fileType}')
                    except Exception as e:
                        db.conn.rollback()
                        logging.error(str(e))
                    if response['status'] == 'success':
                        if preprocess == '1':
                            try:
                                preprocessFileID = response["data"]["preprocessedFileUid"]
                                if preprocessFileID != 'None':
                                    predictFileID = response["data"]["predictedFileUid"]
                                    db.cursor.execute(f"insert into file (`file_id`,`file_name`,`user_id`,`project_id`) values ('{preprocessFileID}','{preprocessFileName}.{fileType}','{userID}','{projectID}');")
                                    db.cursor.execute(f"insert into file (`file_id`,`file_name`,`user_id`,`project_id`) values ('{predictFileID}','{predictFileName}.{fileType}','{userID}','{projectID}');")
                                    db.conn.commit()
                                    return {"status":"success","msg":"predict success","data":{'isPreprocess':'1'}},200
                                else:
                                    predictFileID = response["data"]["predictedFileUid"]
                                    db.cursor.execute(f"insert into file (`file_id`,`file_name`,`user_id`,`project_id`) values ('{predictFileID}','{predictFileName}.{fileType}','{userID}','{projectID}');")
                                    db.conn.commit()
                                    return {"status":"success","msg":"predict success","data":{'isPreprocess':'0'}},200
                            except Exception as e:
                                db.conn.rollback()
                                logging.error(str(e))
                        else:
                            try:
                                predictFileID = response["data"]["predictedFileUid"]
                                db.cursor.execute(f"insert into file (`file_id`,`file_name`,`user_id`,`project_id`) values ('{predictFileID}','{predictFileName}.{fileType}','{userID}','{projectID}');")
                                db.conn.commit()
                                return {"status":"success","msg":"predict success","data":{}},200
                            except Exception as e:
                                db.conn.rollback()
                                logging.error(str(e))
                    else:
                        return response, 400
                else:
                    return {"status":"error","msg":"model id or file id not found","data":{}},500
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()
        else:
            return {"status":"error","msg":"user did not login","data":{}},401