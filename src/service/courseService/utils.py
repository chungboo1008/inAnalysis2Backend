from params import params
import os
import pandas as pd
import glob
import uuid
import logging
from utils import sql

class courseIndexGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        while self.checkModelIndex(self.uid) != ():
            self.uid=str(uuid.uuid1())

    def checkModelIndex(self, modelIndex):
        db=sql()
        db.cursor.execute(f"select * from course where `course_id`='{self.uid}'")
        return db.cursor.fetchall()

class fileChecker():
    def __init__(self,filepath,courseID):
        self.filepath = filepath
        self.filetype = filepath[filepath.rfind("."):]
        self.courseID = courseID

    def studentDataChecker(self):
        try:
            if self.filetype == '.csv':
                data=pd.read_csv(self.filepath)
            # elif self.filetype == '.xls' or self.filetype == 'xlsx':
            #     data=pd.read_excel(self.filepath, index_col=0)

            # check column in csv
            cols=data.columns.tolist()
            if not(' 學號' in cols and ' 電子郵件' in cols):
                raise Exception("[fileChecker] file do not contain 學號 or 電子郵件")
        except Exception as e:
            db=sql()
            db.cursor.execute(f"delete from score where `course_id` = '{self.courseID}'")
            db.conn.commit()
            os.remove(self.filepath)
            raise Exception(f'[fileChecker]{e}')
        return True

class randomIndex():
    def __init__(self,filepath,courseID):
        self.filepath=filepath
        self.filetype=filepath[filepath.rfind("."):]
        self.courseID = courseID

    def randomIndexGenerator(self):
        try:
            if self.filetype == '.csv':
                data=pd.read_csv(self.filepath)
            # elif self.filetype == '.xls' or self.filetype == 'xlsx':
            #     data=pd.read_excel(self.filepath, index_col=0)
            else:
                raise Exception("[fileChecker] file format error")
            db=sql()
            db.cursor.execute(f"delete from score where `course_id` = '{self.courseID}'")
            db.conn.commit()

            # check column in csv
            studentIDList=data[' 學號']
            
            uidList = []
            for studentID in studentIDList:
                uid=str(uuid.uuid1())
                while uid in uidList:
                    uid=str(uuid.uuid1())
                uidList.append(uid)
                tempList = studentIDList
                index = tempList[tempList == studentID].index
                tempList = tempList.drop(index)
                try:
                    db=sql()
                    for ID in tempList:
                        db.cursor.execute(f"insert into score (`course_id`,`judge_id`,`student_id`) values ('{self.courseID}','{studentID}','{ID}');")
                    db.conn.commit()

                except Exception as e:
                    raise Exception(f'[fileChecker]{e}')
                    db.conn.rollback()
                finally:
                    db.conn.close()


            data['StudentUID'] = uidList

            if self.filetype == '.csv':
                data.to_csv(self.filepath)
            # elif self.filetype == '.xls' or self.filetype == '.xlsx':
            #     data.to_excel(self.filepath)

        except Exception as e:
            db=sql()
            db.cursor.execute(f"delete from score where `course_id` = '{self.courseID}'")
            db.conn.commit()
            raise Exception(f'[fileChecker]{e}')
        return True