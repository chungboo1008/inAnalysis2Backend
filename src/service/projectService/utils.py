from params import params
import glob
import uuid
import logging
from utils import sql

class projectUidGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        while self.checkProjectID(self.uid) != ():
            self.uid=str(uuid.uuid1())

    def checkProjectID(self, userUid):
        db=sql()
        db.cursor.execute(f"select * from project where `project_id`='{self.uid}'")
        return db.cursor.fetchall()
