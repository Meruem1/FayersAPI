#!python
import logging,json,os
import pickle
from Session import Session
from fyers_api.Websocket import ws

from fyers_api import fyersModel
from websockets.sync.client import connect
from websocket import create_connection
from fyers_api import accessToken


class loginService :

    def __init__(self) -> None:

        logging.basicConfig(level=logging.DEBUG)
        # LOADING LOGIN DETAILS
        self.__loginCreds = json.load(open("loginInfo.json"))    
        
        # SETTING ACCES TOKEN IN 

        session=accessToken.SessionModel(
        client_id= self.__loginCreds.get("app_id"),
        secret_key= self.__loginCreds.get("secret_key"),
        redirect_uri= self.__loginCreds.get("redirect_uri"), 
        response_type= self.__loginCreds.get("response_type"),
        grant_type= self.__loginCreds.get("grant_type")
        )
        response = session.generate_authcode()
        print("generate_authcode",response)
        self.__authcode = str(input("ENTER YOUR AUTH TOKEN : "))

        session.set_token(self.__authcode)
        response = session.generate_token()
        print("set_token",response)
        self.access_token  = response['access_token']
        self.refresh_token = response['refresh_token']
        print("self.access_token ",self.access_token )
        print("self.refresh_token",self.refresh_token)

        with open("loginInfo.json", "r+") as file:
            temp = json.load(file)
            temp["access_token"] = self.access_token
            temp["refresh_token"] = self.refresh_token
            file.seek(0)
            json.dump(temp, file)

        # writing session to file 
        with open('session.pkl', 'wb') as f:
            pickle.dump(session, f)

       

loginService()        