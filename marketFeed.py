import json,pickle
import asyncio,struct
from datetime import datetime
import six
from fyers_api.Websocket import ws
import threading
from time import strftime, localtime
import SharedArray as sa
import multiprocessing,traceback
import csv
from utils import *

class MarketFeed :
    utilsObj = utils()
    FeedQueueList = multiprocessing.Queue(5000)

    def __init__(self):

        self.__flag = True
        self.loginServiceData = None
        self.access_token =None
        self.data_type = "symbolData"
        self.fs = object()
        self.baseDir = '/root/Vishal/VishalCode/FyersAPI'        
        
        try:
            with open("loginInfo.json", "r") as jsonfile:
                self.loginServiceData = json.load(jsonfile)
        except Exception as e:
            print(e)
            
        try:
            with open("Settings/config.json", "r") as jsonfile:
                self.configData = json.load(jsonfile)
                # print("self.configData",self.configData )
        except Exception as e:
            print(e)
            
        try:
            with open("Settings/feedStruct.json", "r") as jsonfile:
                self.feedStructData = json.load(jsonfile)
        except Exception as e:
            print(e)
            
        self.symbol = list(self.configData.get('symbol').keys())
        # self.symbol =["NSE:FINNIFTY-INDEX"]

        app_id = self.loginServiceData.get('app_id')
        access_token = self.loginServiceData.get('access_token')
        
        self.access_token = app_id +':'+ access_token
        self.fs = ws.FyersSocket(self.access_token,run_background=False,log_path="logs")

        threading.Thread(target=self.getMarketData).start()
        threading.Thread(target=self.saveMarketData).start()
        
        # self.unsubscribe()
        
    def getMarketData(self):
        try:
            self.fs.websocket_data = MarketFeed.custom_message
            self.fs.subscribe(self.symbol ,self.data_type)
        except Exception as e:
            print("getMarketData",e)
            
    def unsubscribe(self):
        print(self.fs,self.symbol)
        self.fs.unsubscribe(symbol=self.symbol)
        
            
    @classmethod
    def custom_message(self,msg):
        try:
            MarketFeed.FeedQueueList.put(msg[0])
            print(datetime.fromtimestamp(msg[0]['timestamp']).strftime("%Y-%m-%d %I:%M:%S"))
            # print(datetime.fromtimestamp(msg[1]['timestamp']).strftime("%Y-%m-%d %I:%M:%S"))
            # print(datetime.fromtimestamp(msg[2]['timestamp']).strftime("%Y-%m-%d %I:%M:%S"))
            
        except Exception as e:
            print("custom_message",e)
            
            
    def saveMarketData(self):
        # save Market Data
        while  self.__flag :
            item = MarketFeed.FeedQueueList.get()
            # print(item)
            try:
                filePath = str(self.baseDir)+'/SharedMemory/'+str(self.configData.get('symbol').get(item['symbol']))
                # print(filePath)
                # if(not os.path.exists(filePath)):
                try:       
                    sa1 = sa.create("file://{}".format(filePath), 5000)
                
                except Exception as e:
                    sa1 = sa.attach("file://"+filePath)
                    sa1[self.feedStructData.get('t')] = item['timestamp']
                    sa1[self.feedStructData.get('s')] = self.configData.get('symbol').get(item['symbol'])
                    sa1[self.feedStructData.get('o')] = item['open_price']
                    sa1[self.feedStructData.get('h')] = item['high_price']
                    sa1[self.feedStructData.get('l')] = item['low_price']
                    sa1[self.feedStructData.get('c')] = item['close_price']
                    sa1[self.feedStructData.get('ltp')] = item['ltp']
                    sa1[self.feedStructData.get('vtt')] = 0
                    
                MarketFeed.utilsObj._csvWriter(str('record/'+str(self.configData.get('symbol').get(item['symbol'])))+'.csv',
                        [
                        item['timestamp'], 
                        self.configData.get('symbol').get(item['symbol']),
                        item['open_price'],
                        item['high_price'], 
                        item['low_price'],
                        item['close_price'],
                        item['ltp'],
                        0
                        ])
        
                # print("sharedTokenArray[self.feeds['ltp']]",sharedTokenArray[self.feeds['ltp']])
                """ delete a instance """
                del sa1
            except Exception as e:
                print("[Error] in (self,saveMarketData) msg: ",str(e))   


        

MarketFeed()