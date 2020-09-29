from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class GetAnalyticsAlgoByProject(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetAnalyticsAlgoByProject] args: {args}")
        projectID = args['projectID']
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            try:
                db=sql()
                db.cursor.execute(f"select * from project where `project_id`='{projectID}'")
                result = db.cursor.fetchone()
                if result != None:
                    form = {
                        "dataType": result[4],
                        "projectType": result[3]
                    }
                    resp = requests.get(coreApi.GetAnalyticAlgo, data=form)
                    response = resp.json()
                    logging.warn(f'response {response}')
                    if response['status'] == 'success':
                        return response,200
                    else:
                        return response,400
                else:
                    return {"status":"error","msg": 'Project not found',"data": {}}, 400

            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg": f'{e}',"data": {}}, 400
                db.conn.rollback()
            finally:
                db.conn.close()
        else:
            return {"status":"error","msg":"user did not login","data":{}},401