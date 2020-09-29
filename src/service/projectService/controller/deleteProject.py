from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
from coreApis import coreApis
from service.model.controller.deleteModel import DeleteModelByProject
import requests
import logging

param=params()
coreApi = coreApis()
deleteModelByProject = DeleteModelByProject()

class DeleteProject(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[DeleteProject] args: {args}")

        projectID = args['projectID']

        #check user isLogin
        if tokenValidator(args['token']):

            try:
                db=sql()
                db.cursor.execute(f"select `file_id` from file where `project_id`='{projectID}'")
                result = db.cursor.fetchall()
                fileIDList = [a[0] for a in result]
                for fileID in fileIDList:
                    form = {
                        'fileUid': fileID,
                        'token': args['token']
                    }
                    response = requests.post( coreApi.DeleteFile, data= form)
                    responseObj = response.json()
                    if responseObj["status"] == "success":
                        db.cursor.execute(f"delete from file where `file_id` = '{fileID}'")
                        db.conn.commit()
                        continue
                    else:
                        return responseObj, 400
                
                if deleteModelByProject.delete(projectID, args['token']) != True:
                    return {"status":"error","msg":"delete project error","data":{}},400
                
                db.cursor.execute(f"delete from project where `project_id` = '{projectID}'")
                db.conn.commit()
                logging.info(f"[DeleteProject] OK with project id {projectID}")
                return {"status":"success","msg":"","data":{}},200

            except Exception as e:
                db.conn.rollback()
                logging.error(e)
                return {"status":"error","msg":f"{e}","data":{}},400
            finally:
                db.conn.close()


        else:
            return {"status":"error","msg":"user did not login","data":{}},401