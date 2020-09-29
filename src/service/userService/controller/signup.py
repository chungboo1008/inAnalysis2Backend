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

param=params()

class Singup(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('account', type=str,required=True)
            parser.add_argument('name', type=str,required=True)
            parser.add_argument('password',type=str,required=True)
            parser.add_argument('email',type=str,required=False)
            args = parser.parse_args()
            logging.info(f'{args}')
            account = args['account']
            name = args['name']
            email = args['email']

            db=sql()
            db.cursor.execute(f"select * from user where `user_account`='{args['account']}' or `user_email`='{email}'")
            result = db.cursor.fetchall()

            if result == ():
                md5 = hashlib.md5()
                md5.update(args['password'].encode("utf-8"))

                password = md5.hexdigest()
                uid = userUidGenerator().uid
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
                        "userID": uid,
                        "account": account,
                        "userName": name,
                        "password": password,
                        "email": email
                    }
                    token = userSignupToken().userSignupTokenGenerator(data)
                    logging.info(token)
                    url = f"{param.frontendurl}/#/signup/{token}"
                    msg = MIMEText(f"<html>Hey {name}!<br> The sign up requires further verification. To complete the sign up, please click the <a href={url}>url</a> to verify.</html>",'html','utf-8')
                    msg['to'] = email
                    msg['from'] = 'inanalysis.github.io@gmail.com'
                    msg['subject'] = "[InAnalysis] Please verify your email"
                    raw = base64.urlsafe_b64encode(msg.as_bytes())
                    raw = raw.decode()
                    body = {'raw': raw}

                    message = (service.users().messages().send(userId="me", body=body).execute())
                    return {"status": "success"}, 200


                except Exception as e:
                    return {"status":"error","msg":str(e),"data":{}},400
                
            else:
                return {"status":"error","msg":"account had been existed","data":{}},400

        except Exception as e:
            return {"status":"error","msg":f"signup error:{e}","data":{}},400
        finally:
            db.conn.close()