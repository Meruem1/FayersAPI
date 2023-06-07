import json,os,pickle
import requests
import pandas as pd

class TradeApi :

    def __init__(self) -> None:
        self.__routes = json.load(open("apiRoutes.json"))

        # loading data from pickle file
        self.__session = None
        with open('session.pkl', 'rb') as f:
            self.__session = pickle.load(f)

        # LOADING ALL THE SESSION STORED IN SESSION.PKL FILE
        try:
            print(f" =======================|| APIKEY : {self.__session.apiKey} || ACCESS_TOKEN : {self.__session.AccessToken} ||=================")
        except Exception as e :
            print(e)
            pass   
        
        self.__header = {
                'X-Kite-Version': '3',
                'Authorization': f'token {self.__session.apiKey}:{self.__session.AccessToken}'
            }


    # ====================================== || INSTRUMENTS AND QUOTES || =============================================

    # TO RETRIEVE ALL INSTRUMENTS FOR TRADING 
    def _getAllInstruments(self,payload={},filename="contracts.csv"):
        try:            
            __response = requests.request(self.__routes.get("getAllInstruments").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getAllInstruments").get("endPoint"), headers=self.__header, data=payload)
            with open(filename, 'w') as temp_file:
                temp_file.write(__response.text)
            return  pd.read_csv(filename)
        except Exception  as e :
            print(e)


    # TO RETRIEVE ALL NSEFO INSTRUMENTS FOR TRADING IN OPTIONS AND FUTURES
    def _getNFOInstruments(self,payload={},filename="nfo_contracts.csv"):
        try:            
            __response = requests.request(self.__routes.get("getNFOInstruments").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getNFOInstruments").get("endPoint"), headers=self.__header, data=payload)
            with open(filename, 'w') as temp_file:
                temp_file.write(__response.text)
            return  pd.read_csv(filename)
        except Exception  as e :
            print(e)

    # TO RETRIEVE ALL NSE stock INSTRUMENTS FOR TRADING IN STOCKs
    def _getNSEInstruments(self,payload={},filename="nse_contracts.csv"):
        try:            
            __response = requests.request(self.__routes.get("getNSEInstruments").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getNSEInstruments").get("endPoint"), headers=self.__header, data=payload)
            with open(filename, 'w') as temp_file:
                temp_file.write(__response.text)
            return  pd.read_csv(filename)
        except Exception  as e :
            print(e)

    # TO GET FULL MARKET QUOTE OF THE PARTICULAR INSTRUMENT IN PARTICULAR EXCHANGE
    def _getFullMarketQuote(self,payload=dict(),params={"i":"NSE:INFY"}):
        try:
            __response = requests.request(self.__routes.get("getFullMarketQuote").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getFullMarketQuote").get("endPoint"),params=params, headers=self.__header, data=payload)           
            return __response.text
        except Exception as e:
            print(e)

    # TO GET OPEN/HIGH/LOW/CLOSE OF THE PARTICULAR INSTRUMENT IN PARTICULAR EXCHANGE
    def _getOHLC(self,payload=dict(),params={"i":"NSE:INFY"}):
        try:
            __response = requests.request(self.__routes.get("getOHLC").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getOHLC").get("endPoint"),params=params,headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e)

    def _getLTP(self,payload=dict(),params={"i":"NSE:INFY"}):
        try:
            __response = requests.request(self.__routes.get("getLTP").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getLTP").get("endPoint"),params=params,headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e)

    # ======================================== || POSITONS AND HOLDINGS || =====================================================

    def _getPositions(self,payload=dict(),params=dict()):
        try:
            __response = requests.request(self.__routes.get("getPositions").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getPositions").get("endPoint"),params=params, headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e)

    def _getHoldings(self,payload=dict(),params=dict()):
        try:
            __response = requests.request(self.__routes.get("getHoldings").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getHoldings").get("endPoint"),params=params, headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e)

    # =========================================== || PROFILE || ==============================================
    
    def _getProfile(self,payload=dict(),params=dict()):
        try:
            __response = requests.request(self.__routes.get("getProfile").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getProfile").get("endPoint"),params=params, headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e)

    def _getFunds(self,payload=dict(),params=dict()):
        try:
            __response = requests.request(self.__routes.get("getFunds").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getFunds").get("endPoint"),params=params, headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e)

    # ========================================= || PLACING ORDERS || =================================================

    def _placeRegularOrder(self,payload=dict(),params=dict()):
        try:
            __response = requests.request(self.__routes.get("placeRegularOrder").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("placeRegularOrder").get("endPoint"),params=params, headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e)

    def _modifyRegularOrder(self,payload=dict(),params=dict(),orderId=0):
        try:
            if orderId == 0 :
                return Exception("please Set orderID")
            __response = requests.request(self.__routes.get("placeRegularOrder").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("placeRegularOrder").get("endPoint")+orderId,params=params, headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e) 

    def _cancelRegularOrder(self,payload=dict(),params=dict(),orderId=0):
        try:
            if orderId == 0 :
                return Exception("please Set orderID")
            __response = requests.request(self.__routes.get("cancelRegularOrder").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("cancelRegularOrder").get("endPoint")+orderId,params=params, headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e) 

    
    def _getRegularOrderList(self,payload=dict(),params=dict()):
        try:
            __response = requests.request(self.__routes.get("getRegularOrderList").get("method"), url=self.__routes.get("baseURL")+self.__routes.get("getRegularOrderList").get("endPoint"),params=params, headers=self.__header, data=payload)
            return __response.text
        except Exception as e:
            print(e) 

    


api = TradeApi()            
print(api._getRegularOrderList())
        