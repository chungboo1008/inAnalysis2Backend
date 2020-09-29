from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class FileService:
    def deleteFile(self, token, fileID):
        form = {
                'fileUid': fileID,
                'token': token
            }
        response = requests.post( coreApi.DeleteFile, data= form)
        responseObj = response.json()
        return responseObj
