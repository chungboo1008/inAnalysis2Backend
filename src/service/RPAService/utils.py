from params import params
import glob
import uuid
import logging
import json
import os
from utils import sql

class RPAUidGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        while self.checkRPAID(self.uid) != ():
            self.uid=str(uuid.uuid1())

    def checkRPAID(self, userUid):
        db=sql()
        db.cursor.execute(f"select * from RPA where `RPA_id`='{self.uid}'")
        return db.cursor.fetchall()

class fileChecker():
    def __init__(self,filepath):
        self.filepath=filepath
        self.param=params()

    def check(self):
        return self.RPAChecker()

    def RPAChecker(self):
        try:
            with open(self.filepath) as json_file:
                data = json_file.read()
            logging.debug(f"[RPAChecker]{data}")
            if not ('centerX' in data):
                raise Exception('json should contain centerX')
            if not ('centerY' in data):
                raise Exception('json should contain centerY')
            if not ('scale' in data):
                raise Exception('json should contain scale')
            if not ('nodes' in data):
                raise Exception('json should contain nodes')
            if not ('links' in data):
                raise Exception('json should contain links')
        except Exception as e:
            os.remove(self.filepath)
            raise Exception(f'[RPAChecker]{e}')
        return True
