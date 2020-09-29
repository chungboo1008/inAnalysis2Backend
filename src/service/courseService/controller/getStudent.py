from flask import session
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging
import pandas as pd

param=params()

class GetStudent(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courseID',type=str,required=True)
        parser.add_argument('studentIndex',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetStudent] args: {args}")
        courseID = args['courseID']
        studentIndex = args['studentIndex']
            
        # resp = []
        try:
            db=sql()
            db.cursor.execute(f"select * from course where `course_id`='{courseID}'")
            result = db.cursor.fetchall()
            data=[list(a) for a in result]
            for item in data:
                respItem = {
                    'courseName': item[1],
                    'courseYear': item[2],
                    'jobName': item[3],
                    'deadline': item[4]
                }
                data=pd.read_csv('./src/student/'+courseID+'.csv')
                studentUIDList = data['StudentUID'].tolist()
                if studentIndex not in studentUIDList:
                    return {"status":"error","msg":"studentIndex not exist","data":{}},400
                studentID = data[data['StudentUID'] == studentIndex][' 學號'].values[0]
                data = data[data['StudentUID'] != studentIndex]
                colNames=data.columns.tolist()
                if 'index' in colNames:
                    # sort by index
                    data = data.sort_values(by='index')
                    indexList = data['index'].tolist()
                studentIDList = data[' 學號'].tolist()
                studentNameList = data[' 姓名'].tolist()
                respItem['score']={}
                db.cursor.execute(f"select student_id, score from score where `course_id`='{courseID}' AND `judge_id`= '{studentID}'")
                scoreResult = db.cursor.fetchall()
                scoreDataList=[list(a) for a in scoreResult]
                respItem['score'][f'{studentID}']={}
                for scoreData in scoreDataList:
                    if 'index' in colNames:
                        respItem['score'][f'{studentID}'][f'{scoreData[0]}'] = {
                            'name': studentNameList[studentIDList.index(f'{scoreData[0]}')],
                            'score': scoreData[1],
                            'index': indexList[studentIDList.index(f'{scoreData[0]}')]
                        }
                    else:
                        respItem['score'][f'{studentID}'][f'{scoreData[0]}'] = {
                            'name': studentNameList[studentIDList.index(f'{scoreData[0]}')],
                            'score': scoreData[1]
                        }
        except Exception as e:
            logging.error(str(e))
            db.conn.rollback()
        finally:
            db.conn.close()
        logging.debug(f"[GetStudent] resp: {respItem}")
        return {"status":"success","msg":"","data":{'course': respItem}},200