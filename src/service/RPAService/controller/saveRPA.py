from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from service.RPAService.utils import RPAUidGenerator
import logging
import requests
import json

param=params()

class SaveRPA(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userID', type=str, required=True)
        parser.add_argument('projectID', type=str, required=True)
        parser.add_argument('RPAJson', type=str, required=True)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[saveRPA] args: {args}")

        userID = args['userID']
        projectID = args['projectID']
        RPAJson = args['RPAJson']
        token = args['token']
        description = args['description']
        name = args['name']

        #check user isLogin
        if tokenValidator(token):
            uid = RPAUidGenerator().uid
            with open(param.RPAFilepath +'\\'+ uid + '.json', 'w') as json_file:
                # json.dump(RPAJson, json_file)
                json_file.write(RPAJson)
            try:
                db=sql()
                db.cursor.execute(f"select MAX(version) from RPA where `project_id`='{projectID}'")
                result,  = db.cursor.fetchone()
                if result == None:
                    version = 1
                    
                else:
                    version = result + 1
                    if (name == '' or description == ''):
                        db.cursor.execute(f"select * from RPA where `project_id`='{projectID}' AND `top_version`='Y'")
                        result = db.cursor.fetchone()
                        if (name == ''):
                            name = result[6]
                        if (description == ''):
                            description = result[5]
                    db.cursor.execute(f"update RPA set `top_version`='N' where `user_id` = '{userID}' and `project_id` = '{projectID}'")
                    db.conn.commit()
                db.cursor.execute(f"insert into RPA (`user_id`,`project_id`, `version`, `RPA_id`, `top_version`, `description`, `name`) values ('{userID}','{projectID}','{version}','{uid}','Y', '{description}', '{name}');")
                db.conn.commit()
                return {"status":"success","msg":"","data":{"RPAID":uid}},201
            except Exception as e:
                logging.debug(f"[saveRPA] error: {e}")
                db.conn.rollback()
                return {"status":"error","msg":"","data":{}},400
            finally:
                db.conn.close()  
        else:
            return {"status":"error","msg":"user did not login","data":{}},401