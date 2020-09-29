from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class AnalyticService():
    def doModelTrain(self, token, fileUid, dataType, projectType, algoName, param, input, output):
        form = {
            'token': token,
            'fileUid': fileUid,
            'dataType': dataType,
            'projectType': projectType,
            'algoName': algoName,
            'param': param,
            'input': input,
            'output': output
        }  
        resp = requests.post(coreApi.DoModelTrain, data=form)
        response = resp.json()
        return response

    def doPreprocess(self, token, fileID, action):
        form = {
            'fileUid': fileID,
            'action': action,
            'token': token
        }
        resp = requests.post(coreApi.DoPreprocess, data=form)
        response = resp.json()
        return response

    def doCorrelation(self, fileID, correlationAlgoName, token):
        try:
            form = {
                'fileUid': fileID,
                'algoname': correlationAlgoName,
                'token': token
            }            
            resp = requests.post(coreApi.DoCorrelation, data=form)
            response = resp.json()
            return response
        except Exception as e:
            logging.error(str(e))
            return response

    def doModelPredict(self, token, modelUid, fileID, preprocess ):
        try:
            form = {
                'modelUid': modelUid,
                'fileUid': fileID,
                'preprocess': preprocess,
                'token': token
            }            
            resp = requests.post(coreApi.DoModelPredict, data=form)
            response = resp.json()
            return response
        except Exception as e:
            return {"status":"error","msg":f"{e}","data":{}},500

    def doModelTest(self, token, modelUid, fileID, label):
        try:
            form = {
                'modelUid': modelUid,
                'fileUid': fileID,
                'label': label,
                'token': token
            }            
            resp = requests.post(coreApi.DoModelTest, data=form)
            response = resp.json()
            return response
        except Exception as e:
            return {"status":"error","msg":f"{e}","data":{}},500

    def getModelPreview(self, token, modelUid):
        try:
            form = {
                'modelUid': modelUid,
                'token': token
            }            
            resp = requests.get(coreApi.GetModelPreview, data=form)
            response = resp.json()
            return response
        except Exception as e:
            return {"status":"error","msg":f"{e}","data":{}},500