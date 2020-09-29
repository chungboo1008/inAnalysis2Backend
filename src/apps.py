import os
from flask import Flask, request, abort
from flask_restful import Api
from flask_cors import CORS
from service.systemService.controller.getDataProject import GetDataProject
from service.systemService.controller.getDataFile import GetDataFile
from service.userService.controller.signin import Singin
from service.userService.controller.signup import Singup
from service.userService.controller.signupVerify import SingupVerify
from service.userService.controller.generateToken import GenerateToken
from service.userService.controller.getUserInfo import GetUserInfo
from service.userService.controller.forgetPassword import ForgetPassword
from service.userService.controller.forgetPasswordVerify import ForgetPasswordVerify
from service.file.controller.upload import Upload
from service.file.controller.getFileList import GetFileList
from service.file.controller.delete import DeleteFile
from service.file.controller.download import DownloadFile
from service.file.controller.getColumn import GetFileColumn
from service.projectService.controller.addProject import AddProject
from service.projectService.controller.getProjectByUser import GetProjectByUserID
from service.projectService.controller.deleteProject import DeleteProject
from service.projectService.controller.getProjectInfo import GetProjectInfo
from service.visualizeService.controller.getVisAlgoList import GetVisAlgoList
from service.visualizeService.controller.dataViz import dataViz
from service.analytic.controller.getPreprocessAlgo import GetPreprocessAlgoList
from service.analytic.controller.getCorrelationAlgo import GetCorrelationAlgoList
from service.analytic.controller.doPreprocess import DoPreprocess
from service.analytic.controller.doCorrelation import DoCorrelation
from service.analytic.controller.doCorrelationByFile import DoCorrelationByFile
from service.analytic.controller.previewPreprocess import PreviewPreprocess
from service.analytic.controller.getAnalyticAlgoByProject import GetAnalyticsAlgoByProject
from service.analytic.controller.getAnalyticAlgoParam import GetAnalyticAlgoParam
from service.analytic.controller.doModelTrain import DoModelTrain
from service.analytic.controller.doModelTrainByFile import DoModelTrainByFile
from service.analytic.controller.getModelPreview import GetModelPreview
from service.analytic.controller.doModelTest import DoModelTest
from service.analytic.controller.doModelPredict import DoModelPredict
from service.analytic.controller.stopTraining import StopTraining
from service.analytic.controller.getModelParameter import GetModelParameter
from service.model.controller.addModel import AddModel
from service.model.controller.getModelByProject import GetModelByProjectID
from service.model.controller.deleteModel import DeleteModel
from service.model.controller.deleteModelByUid import DeleteModelUID
from service.courseService.controller.addCourse import AddCourse
from service.courseService.controller.uploadStudentFile import UploadStudentFile
from service.courseService.controller.getCourse import GetCourse
from service.courseService.controller.deleteCourse import DeleteCourse
from service.courseService.controller.getCourseByID import GetCourseByID
from service.courseService.controller.modifyCourse import ModifyCourse
from service.courseService.controller.getStudent import GetStudent
from service.courseService.controller.judge import Judge
from service.courseService.controller.sendEmail import SendEmail
from service.RPAService.controller.saveRPA import SaveRPA
from service.RPAService.controller.loadRPA import LoadRPA
from service.RPAService.controller.exportRPA import ExportRPA
from service.RPAService.controller.importRPA import ImportRPA
from service.RPAService.controller.runRPA import RunRPA
from service.RPAService.controller.getRPA import GetRPA
from service.RPAService.controller.searchRPA import SearchRPA
from datetime import timedelta
import logging
import sys
sys.dont_write_bytecode = True #disable __pycache__
from params import params

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

param=params()
app = Flask(__name__)
app.config['SECRET_KEY'] = param.secretKey
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
api = Api(app)
cors = CORS(app)

line_bot_api = LineBotApi('2bgWsnCNsHxgZ84kQC8OUY/1Xnw1g3cKM4q8L7bOUqi4a3qgr80p8uY/2C0ynPZ/zbS3+vLpGT3zvNbESL+cQbkTY7vVlygpQ4wa/P6aHIbONoZLrI55oRAB4gftkPKk/rWiag0gGwGRTdJ3xQCulQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fc6da215620b26fb6c6336537233c0b9')


@app.route("/callback", methods=['POST'])
def callback():
    print('here')
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))



# bind api
api.add_resource(GetDataProject, "/system/getDataProject")
api.add_resource(GetDataFile, "/system/getDataFile")

api.add_resource(Singin, "/user/signin")
api.add_resource(Singup, "/user/signup")
api.add_resource(SingupVerify, "/user/signupVerify")
api.add_resource(GenerateToken, "/user/generateToken")
api.add_resource(GetUserInfo, "/user/getUserInfo")
api.add_resource(ForgetPassword, "/user/forgetPassword")
api.add_resource(ForgetPasswordVerify, "/user/forgetPasswordVerify")

api.add_resource(Upload, '/file/upload')
api.add_resource(GetFileList, '/file/getFileList')
api.add_resource(DeleteFile, '/file/delete')
api.add_resource(DownloadFile, '/file/download')
api.add_resource(GetFileColumn, '/file/getColumn')

api.add_resource(AddProject, '/project/add')
api.add_resource(GetProjectByUserID, '/project/getProjectByUserID')
api.add_resource(DeleteProject, '/project/delete')
api.add_resource(GetProjectInfo, '/project/getProjectInfo')

api.add_resource(GetVisAlgoList, '/visualize/getAlgo')
api.add_resource(dataViz, '/visualize/doVisualize')
api.add_resource(GetPreprocessAlgoList, '/analytic/getPreprocessAlgo')
api.add_resource(GetCorrelationAlgoList, '/analytic/getCorrelationAlgo')
api.add_resource(DoPreprocess, '/analytic/doPreprocess')
api.add_resource(DoCorrelation, '/analytic/doCorrelation')
api.add_resource(DoCorrelationByFile, '/analytic/DoCorrelationByFile')
api.add_resource(PreviewPreprocess, '/analytic/preprocessPreview')
api.add_resource(GetAnalyticsAlgoByProject, '/analytic/getAnalyticsAlgoByProject')
api.add_resource(GetAnalyticAlgoParam, '/analytic/getAnalyticAlgoParam')
api.add_resource(DoModelTrain, '/analytic/doModelTrain')
api.add_resource(DoModelTrainByFile, '/analytic/doModelTrainByFile')
api.add_resource(DoModelTest, '/analytic/doModelTest')
api.add_resource(GetModelPreview, '/analytic/getModelPreview')
api.add_resource(DoModelPredict, '/analytic/doModelPredict')
api.add_resource(StopTraining, '/analytic/stopModelTraining')
api.add_resource(GetModelParameter, '/analytic/getModelParameter')

api.add_resource(AddModel, '/model/addModel')
api.add_resource(GetModelByProjectID, '/model/getModelByProjectID')
api.add_resource(DeleteModel, '/model/deleteModel')
api.add_resource(DeleteModelUID, '/model/deleteModelUID')

# Api for RPA
api.add_resource(SaveRPA, '/RPA/saveRPA')
api.add_resource(LoadRPA, '/RPA/loadRPA')
api.add_resource(ExportRPA, '/RPA/exportRPA')
api.add_resource(ImportRPA, '/RPA/importRPA')
api.add_resource(RunRPA, '/RPA/runRPA')
api.add_resource(GetRPA, '/RPA/getRPA')
api.add_resource(SearchRPA, '/RPA/searchRPA')

# Api for TA
api.add_resource(UploadStudentFile, '/course/uploadStudentFile')
api.add_resource(AddCourse, '/course/addCourse')
api.add_resource(GetCourse, '/course/getCourse')
api.add_resource(DeleteCourse, '/course/deleteCourse')
api.add_resource(GetCourseByID, '/course/getCourseByID')
api.add_resource(ModifyCourse, '/course/modifyCourse')
api.add_resource(GetStudent, '/course/getStudent')
api.add_resource(Judge, '/course/studentJudge')
api.add_resource(SendEmail, '/course/sendEmail')

# Api for Linebot
# api.add_resource(GetMessage, '/callback')

if __name__ == "__main__":
    if '--debug' in sys.argv:
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO , format='[%(levelname)s] %(message)s')
    logging.info(f'Inanalysis running at port {param.port}')
    app.run(debug='--debug' in sys.argv,port=param.port,host=param.host)
