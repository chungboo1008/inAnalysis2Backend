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
from service.userService.utils import userPasswordToken
import hashlib
import glob
import uuid
import logging

param=params()

class ForgetPassword(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('account', type=str,required=True)
            args = parser.parse_args()
            logging.info(f'Forget password {args}')
            account = args['account']

            db=sql()
            db.cursor.execute(f"select * from user where `user_account`='{args['account']}'")
            result = db.cursor.fetchone()

            if result != None:
                try:
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
                    data = {
                        "userID": result[0],
                        "account": result[2],
                    }
                    token = userPasswordToken().userPasswordTokenGenerator(data)
                    logging.info(token)
                    url = f"{param.frontendurl}/#/password/{token}"
                    msg = MIMEText(f"<html>Hey {account}!<br> Forgot password attempt requires further verification. To complete the attempt, please click the <a href={url}>url</a> to verify.</html>",'html','utf-8')
                    msg['to'] = result[3]
                    msg['from'] = 'inanalysis.github.io@gmail.com'
                    msg['subject'] = "[InAnalysis] Please verify your identity"
                    raw = base64.urlsafe_b64encode(msg.as_bytes())
                    raw = raw.decode()
                    body = {'raw': raw}

                    message = (service.users().messages().send(userId="me", body=body).execute())
                    return {"status": "success"}, 200


                except Exception as e:
                    return {"status":"error","msg":str(e),"data":{}},400
                
            else:
                return {"status":"error","msg":"account not existed","data":{}},400

        except Exception as e:
            return {"status":"error","msg":f"signup error:{e}","data":{}},400
        finally:
            db.conn.close()