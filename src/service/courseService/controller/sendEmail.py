from email.mime.text import MIMEText
import base64
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
from service.userService.utils import userUidGenerator, userSignupToken
import hashlib
import glob
import uuid
import logging
import pandas as pd

param=params()

class SendEmail(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courseID', type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.info(f'{args}')
        courseID = args['courseID']
        token = args['token']


        if tokenValidator(token):
            try:
                db=sql()
                db.cursor.execute(f"select course_name from course where `course_id`='{courseID}'")
                result = db.cursor.fetchall()
                courseData=[list(a) for a in result]
                for item in courseData:
                    courseName = item[0]
                data=pd.read_csv('./src/student/'+courseID+'.csv')
                
                for index, row in data.iterrows():
                    studentIndex = row['StudentUID']
                    email = row[' 電子郵件']
                    # If modifying these scopes, delete the file token.pickle.
                    SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://mail.google.com/']
                    creds=None
                    if os.path.exists('google_token.pickle'):
                        with open('google_token.pickle', 'rb') as token:
                            creds = pickle.load(token)
                    if not creds or not creds.valid:
                        if creds and creds.expired and creds.refresh_token:
                            creds.refresh(Request())
                        else:
                            flow = InstalledAppFlow.from_client_secrets_file(
                                'client_secret.json', SCOPES)
                            creds = flow.run_local_server(port=0)
                        # Save the credentials for the next run
                        with open('google_token.pickle', 'wb') as token:
                            pickle.dump(creds, token)
                    service = build('gmail', 'v1', credentials=creds)
                    url = f"{param.frontendurl}/#/judge/{courseID}/{studentIndex}"
                    msg = MIMEText(f"<html><br>請點擊<a href={url}>連結</a>進行課堂互評。<br>每個人的評分連結不同，請勿分享</html>",'html','utf-8')
                    msg['to'] = email
                    msg['from'] = 'inanalysis.github.io@gmail.com'
                    msg['subject'] = f"{courseName}課堂互評網址"
                    raw = base64.urlsafe_b64encode(msg.as_bytes())
                    raw = raw.decode()
                    body = {'raw': raw}

                    message = (service.users().messages().send(userId="me", body=body).execute())
                return {"status": "success"}, 200


            except Exception as e:
                return {"status":"error","msg":str(e),"data":{}},400
        else:
            return {"status":"error","msg":"user did not login","data":{}},401