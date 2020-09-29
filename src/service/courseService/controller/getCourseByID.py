from flask import session
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging
import pandas as pd
import os

param=params()

class GetCourseByID(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courseID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()

        courseID = args['courseID']
        logging.debug(f"[GetCourseByID] args: {args}")

        #check user isLogin
        if tokenValidator(args['token']):
            
            resp = []
            try:
                db=sql()
                db.cursor.execute(f"select * from course where `course_id`='{courseID}'")
                result = db.cursor.fetchall()
                data=[list(a) for a in result]
                for item in data:
                    respItem = {
                        'courseID': item[0],
                        'courseName': item[1],
                        'courseYear': item[2],
                        'jobName': item[3],
                        'deadline': item[4]
                    }
                    filepath = './src/student/'+courseID+'.csv'
                    if os.path.isfile(filepath):
                        data=pd.read_csv(filepath)
                        studentIDList = data[' 學號']
                        respItem['studentList']=studentIDList.tolist()
                        respItem['scoreList']={}
                        for studentID in studentIDList:
                            db.cursor.execute(f"select student_id, score from score where `course_id`='{courseID}' AND `judge_id`= '{studentID}'")
                            scoreResult = db.cursor.fetchall()
                            scoreDataList=[list(a) for a in scoreResult]
                            respItem['scoreList'][f'{studentID}']={}
                            for scoreData in scoreDataList:
                                respItem['scoreList'][f'{studentID}'][f'{scoreData[0]}'] = scoreData[1]

                    resp.append(respItem)
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()
            logging.debug(f"[GetCourseByID] resp: {resp}")
            return {"status":"success","msg":"","data":{'course': resp}},200


        else:
            return {"status":"error","msg":"user did not login","data":{}},401