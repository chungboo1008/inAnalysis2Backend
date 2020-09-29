from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
from service.projectService.utils import projectUidGenerator
import logging

param=params()

class AddProject(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectName', type=str, required=True)
        parser.add_argument('projectType',type=str,required=True)
        parser.add_argument('dataType',type=str,required=True)
        parser.add_argument('userID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[AddProject] args: {args}")

        projectName = args['projectName']
        projectType = args['projectType']
        dataType = args['dataType']
        userID = args['userID']

        #check user isLogin
        if tokenValidator(args['token']):

            projectTypeList=param.projectTypeList
            #check project type
            if args['projectType'] not in projectTypeList:
                return {"status":"error","msg":"project type not supported","data":{}},400

            
            dataTypeList=param.dataFileTypeList
            #check data type
            if dataType not in dataTypeList:
                return {"status":"error","msg":"data type not supported","data":{}},400

            uid = projectUidGenerator().uid
            try:
                db=sql()
                db.cursor.execute(f"insert into project (`project_id`,`user_id`,`project_name`,`project_type`,`data_type`) values ('{uid}','{userID}','{projectName}','{projectType}','{dataType}');")
                db.conn.commit()
            except Exception as e:
                db.conn.rollback()
            finally:
                db.conn.close()
            logging.info(f"[AddProject] OK with project id {uid}")
            return {"status":"success","msg":"","data":{"projectID":uid}},201


        else:
            return {"status":"error","msg":"user did not login","data":{}},401