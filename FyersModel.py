from fyers_api import fyersModel
import json

class FyersModel :

    def __init__(self) -> None:
        
        self.__loginCreds = json.load(open("loginInfo.json"))        
        self.client_id = self.__loginCreds.get("app_id")
        self.access_token = self.__loginCreds.get("access_token")

        self.modelObj = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token)
    
    def getHistoricalData(self):
            
        data = {
            "symbol":"NSE:SBIN-EQ",
            "resolution":"D",
            "date_format":"0",
            "range_from":"1622097600",
            "range_to":"1622097685",
            "cont_flag":"1"
        }

        response = self.modelObj.history(data=data)
        print(response)
        
FyersModel().getHistoricalData()