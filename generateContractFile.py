from utilities import Utilities
import pandas as pd
import os
import datetime
import json
import string
import SharedArray
import shutil
# from customDecoration import timer
class ContractFile(Utilities):
    def __init__(self):
        super().__init__()
        self.createContractFile()

        
    # @timer    
    def createContractFile(self):
        result=pd.DataFrame(self.kite.instruments())
        result.rename(columns={'name':'contract_name','strike':'strike_price','instrument_type':'option_type','tradingsymbol':'ticker_code','instrument_token':'token'},inplace=True)
        result['expiry']=result['expiry'].apply(lambda x : f"{datetime.datetime.strptime(str(x).strip(),'%Y-%m-%d'):%d%b%Y}" if str(x).strip()!='' else str(x).strip())
        result['security_type']=result['segment']
        result['FNO'] ='NA'
        result['divider']=100
        result['multiplier']=1
        result['currency']='INR'
        result['strike_price']=result['strike_price']*result['divider']
        result['tokenID'] = result['exchange']+ result['segment']+result['token'].astype(str)
        
        result.loc[(result['exchange'] == 'BCD') & (result['segment'] == 'BCD-OPT'), ['tokenID2']]=str(self.contractSettings.get('BCD').get('ID'))+str(self.contractSettings.get('BCD').get('BCD-OPT'))+result['token'].astype(str)
        result.loc[(result['exchange'] == 'BCD') & (result['segment'] == 'BCD-FUT'), ['tokenID2']]=str(self.contractSettings.get('BCD').get('ID'))+str(self.contractSettings.get('BCD').get('BCD-FUT'))+result['token'].astype(str)
        result.loc[(result['exchange'] == 'BCD') & (result['segment'] == 'BCD'), ['tokenID2']]=str(self.contractSettings.get('BCD').get('ID'))+str(self.contractSettings.get('BCD').get('BCD'))+result['token'].astype(str)
        
        result.loc[(result['exchange'] == 'BSE') & (result['segment'] == 'INDICES'), ['tokenID2']]=str(self.contractSettings.get('BSE').get('ID'))+str(self.contractSettings.get('BSE').get('INDICES'))+result['token'].astype(str)
        result.loc[(result['exchange'] == 'BSE') & (result['segment'] == 'BSE'), ['tokenID2']]=str(self.contractSettings.get('BSE').get('ID'))+str(self.contractSettings.get('BSE').get('BSE'))+result['token'].astype(str)
        
        result.loc[(result['exchange'] == 'MCX') & (result['segment'] == 'MCX-OPT'), ['tokenID2']]=str(self.contractSettings.get('MCX').get('ID'))+str(self.contractSettings.get('MCX').get('MCX-OPT'))+result['token'].astype(str)
        result.loc[(result['exchange'] == 'MCX') & (result['segment'] == 'MCX-FUT'), ['tokenID2']]=str(self.contractSettings.get('MCX').get('ID'))+str(self.contractSettings.get('MCX').get('MCX-FUT'))+result['token'].astype(str)
        result.loc[(result['exchange'] == 'MCX') & (result['segment'] == 'INDICES'), ['tokenID2']]=str(self.contractSettings.get('MCX').get('ID'))+str(self.contractSettings.get('MCX').get('INDICES'))+result['token'].astype(str)

        result.loc[(result['exchange'] == 'NSE') & (result['segment'] == 'INDICES'), ['tokenID2']]=str(self.contractSettings.get('NSE').get('ID'))+str(self.contractSettings.get('NSE').get('INDICES'))+result['token'].astype(str)
        result.loc[(result['exchange'] == 'NSE') & (result['segment'] == 'NSE'), ['tokenID2']]=str(self.contractSettings.get('NSE').get('ID'))+str(self.contractSettings.get('NSE').get('NSE'))+result['token'].astype(str)
        
        result.loc[(result['exchange'] == 'CDS') & (result['segment'] == 'CDS-OPT'), ['tokenID2']]=str(self.contractSettings.get('CDS').get('ID'))+str(self.contractSettings.get('CDS').get('CDS-OPT'))+result['token'].astype(str)
        result.loc[(result['exchange'] == 'CDS') & (result['segment'] == 'CDS-FUT'), ['tokenID2']]=str(self.contractSettings.get('CDS').get('ID'))+str(self.contractSettings.get('CDS').get('CDS-FUT'))+result['token'].astype(str)
        
        result.loc[(result['exchange'] == 'NFO') & (result['segment'] == 'NFO-FUT'), ['tokenID2']]=str(self.contractSettings.get('NFO').get('ID'))+str(self.contractSettings.get('NFO').get('NFO-FUT'))+result['token'].astype(str)
        result.loc[(result['exchange'] == 'NFO') & (result['segment'] == 'NFO-OPT'), ['tokenID2']]=str(self.contractSettings.get('NFO').get('ID'))+str(self.contractSettings.get('NFO').get('NFO-OPT'))+result['token'].astype(str)
        
        # print(result.loc[(result['exchange'] == 'NFO')]['tokenID2'])
        # Create Contract FOLDER
        try:
            os.makedirs(self.baseDir+'contracts')
        except Exception as e:
            pass

        # this is for store contracts file in store folder
        try:
            os.makedirs(self.baseDir+'store')
        except Exception as e:
            pass

        try:
            os.makedirs(self.baseDir+'store/contracts')
        except Exception as e:
            pass

        result['tokenID2']=result['tokenID2'].apply(lambda x: self.concateDecToDec(x))
        

        result.to_csv(self.baseDir+'store/contracts/zerodha_contractfile'+str(datetime.datetime.now().strftime('%Y%m%d'))+'.csv')

        forJson=result.to_dict('records')
        forJsonPath=self.baseDir+'store/contracts/zerodha_contractfile'+str(datetime.datetime.now().strftime('%Y%m%d'))+'.json'
        self.createSharedArray(forJson)

        if not os.path.exists(forJsonPath):
            with open(forJsonPath, "w") as file:
                json.dump({}, file)

        with open(forJsonPath,"w") as file :
        # with open(filedirect, "r+") as file:
            # temp = json.load(file)
            temp = {}
            for i in forJson:
                # i['expiry']=str(i.get('expiry')).strip()
                temp[i.get('tokenID2')] = i
                # print(temp)
            file.seek(0)
            json.dump(temp, file)

        segmentList=result['segment'].drop_duplicates()
        segmentList=segmentList.values

        alphaLetter=list(string.ascii_uppercase)
        for j in segmentList:
            try:
                shutil.rmtree(self.baseDir+'contracts/'+j)
            except Exception as e:
                pass

            try:
                os.makedirs(self.baseDir+'contracts/'+j)
            except Exception as e:
                pass

            for i in alphaLetter:
                temp=result.loc[(result['ticker_code'].str.startswith(i,na=False)) & (result['segment']==j)]
                # print(temp)
                if temp.shape[0]>0:
                    temp.to_csv(f"""{self.baseDir}contracts/{j}/{i}.csv""")
                    filename = os.path.join(f"""{self.baseDir}contracts/{j}/{i}.json""")
                    with open(filename,"w") as file :
                        json.dump(temp.to_dict('records'),file) 

    def createSharedArray(self,data):
        for i in data:
            try:
                os.makedirs(self.baseDir+'tickers')
            except Exception as e:
                pass

            try:       
                tickerpath=f"""file://{self.baseDir[:-1]}{self.jsonConfigfile.get('settings').get('fileLocation').get('tickers')}{str(i.get("tokenID2"))}"""
                # print(tickerpath)
                sa = SharedArray.create(tickerpath, 1000)
            except Exception as e:
                pass
                # print("Error on createSharedArray",e)

ContractFile()