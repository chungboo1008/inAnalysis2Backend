from params import params
import glob
import uuid
import logging
from utils import sql

class modelIndexGenerator():
    def __init__(self):
        self.index=str(uuid.uuid1())
        while self.checkModelIndex(self.index) != ():
            self.index=str(uuid.uuid1())

    def checkModelIndex(self, modelIndex):
        db=sql()
        db.cursor.execute(f"select * from model where `model_index`='{self.index}'")
        return db.cursor.fetchall()
