import json,os,pickle
import requests
import pandas as pd
from datetime import datetime, timedelta
from utils import * 

class FyersAPI :

    def __init__(self) -> None:
        self.util_obj = utils()
        
        self.__loginCreds = json.load(open("loginInfo.json"))    
        self.__config = json.load(open("Settings/config.json"))     
        
        symlist = self.__config.get('symbol') 
            
          
        self.__header = {
            'Authorization': f'{self.__loginCreds.get("app_id")}:{self.__loginCreds.get("access_token")}',
            'Content-Type': 'application/json'
        }
        
        self.historicalDuration = 15
        self.historicalDays = 99

        self.historicalStartDate = (datetime.today() - timedelta(days=self.historicalDays)).strftime('%Y-%m-%d')
        self.historicalEndDate = datetime.today().strftime('%Y-%m-%d')
        
        print(self.historicalStartDate,self.historicalEndDate)
        
        self.__routes = json.load(open("FyersApiRoutes.json"))
        
        self._getNSEInstruments("getNSECD","nsecd_contracts.csv")
        self._getNSEInstruments("getNSECM","nsecm_contracts.csv")
        self._getNSEInstruments("getNSEFO","nsefo_contracts.csv")
        
        for key,val in symlist.items():
            self._getHistoricalData({
                'symbol':key,
                'resolution':self.historicalDuration,
                'date_format':1,
                'range_from':self.historicalStartDate,
                'range_to':self.historicalEndDate,
                'cont_flag':''
            },str(val))
        
        
    # TO RETRIEVE ALL NSEFO INSTRUMENTS FOR TRADING IN NSECD
    def _getNSEInstruments(self,route,filename):
        try:            
            __response = requests.request(self.__routes.get(route).get("method"), url=self.__routes.get("ContractFileURL")+self.__routes.get(route).get("endPoint"))
            with open("contracts/"+filename, 'w') as temp_file:
                temp_file.write(__response.text)
            # df = pd.read_csv(temp_file)
            # print(df)
            # df.columns = ['token','symbol']
            # df.to_csv("contracts/"+filename)
            # print(df)
            # return  pd.read_csv(os.getcwd()+"/contracts/"+filename)
        except Exception  as e :
            print(e)
            

    def _placeRegularOrder(self,params = {},payload=dict()):
        try:
            __response = requests.request(self.__routes.get("placeOrders").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("placeOrders").get("endPoint"), headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e)
            
            
    def _getHistoricalData(self,params = {},symbol=''):
        try:
            print("++++++++++",params,symbol)
            __response = requests.request(self.__routes.get("getHistoricalData").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getHistoricalData").get("endPoint"), headers=self.__header, params=params)
            # print(json.loads(__response.text))
            mylist = json.loads(__response.text)['candles']
            columns =["timestamp","open","high","low","close","vtt"]
            df = pd.DataFrame(mylist,columns=columns)
            df['symbol'] = symbol
            # df = self.util_obj._calculateRSI(df)
            df.to_csv("historical/"+symbol+".csv")
        except Exception as e:
            print(e)
            
   
        
obj = FyersAPI()
