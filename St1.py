import json,threading
import SharedArray as sa
from datetime import datetime
from time import strftime, localtime
from utils import *
import os 

class st1:
    def __init__(self):
        util_obj = utils()
        self.__flag = True
        self.baseDir = '/root/Vishal/VishalCode/FyersAPI'    
        
        self.starttime=int(9)*60+int(15)
        self.timeinterval=15
        print("before",self.starttime,self.starttime/60)
        self.starttime=self.setStartTime(self.starttime,self.timeinterval)
        print("after",self.starttime)
        hours = str(int(self.starttime/60))
        minutes=str(self.starttime%60)

        if(len(minutes) < 2 ):
            minutes = minutes+'0'
             
        self.candleTime = hours+":"+minutes+":00"
        print("hours , minutes",hours+":"+minutes)
        
        try:
            with open("Settings/St1.json", "r") as jsonfile:
                self.St1Data = json.load(jsonfile)
                print(self.St1Data['symbol'])
        except Exception as e:
            print(e)
            
        for key,val in self.St1Data['symbol'].items():
            # print(key,val)
            threading.Thread(target=self.getMarketData , args =(val,)).start()
            

    def getMarketData(self,i):
        print("***********",i)
        # save Market Data
        filePath = str(self.baseDir)+'/SharedMemory/'+str(i)
        if(os.path.exists(filePath)):
            sta = sa.attach("file://"+filePath)

            print(strftime('%Y-%m-%d %H:%M:%S', localtime(sta[0])),sta[1])
            print("self.candleTime",self.candleTime)
            # while  self.__flag :
            #     print(strftime('%Y-%m-%d %H:%M:%S', localtime(sta[0])),sta[1])
                
                # print(sta[0],sta[1],sta[2],sta[3],sta[4],sta[5])
            
        
        
    def setStartTime(self,starttime,timeinterval):
        current=int(datetime.now().hour)*60+int(datetime.now().minute)
        # current=int(20)*60+int(25)
        current = current - starttime
        while current%timeinterval != 0:
            current = current + 1
        return starttime + current

st1()
            