
from os.path import expanduser
from datetime import date,datetime,timedelta
import utils 

print(expanduser("~")+'/Vishal/VishalCode/FyersAPI')

class generalCon:
    def __init__(self):
        utilsObj = utils()
        self.baseDir= expanduser("~")+'/Vishal/VishalCode/FyersAPI'
        self.todayDate = str(date.today()).replace('-','')

        utilsObj.createFolder(self.baseDir,'contracts')
        utilsObj.createFolder(self.baseDir,'hisotrical')
        utilsObj.createFolder(self.baseDir,'record')
        utilsObj.createFolder(self.baseDir,'results')
        utilsObj.createFolder(self.baseDir,'Settings')
        utilsObj.createFolder(self.baseDir,'SharedMemory')
        
