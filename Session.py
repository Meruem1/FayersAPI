class Session : 

    def __init__(self,**kwargs) :
        self.__refreshToken = kwargs.get("refreshToken","")
        self.__accessToken = kwargs.get("accessToken","")
        self.__apiKey = kwargs.get("apiKey","")
        self.__secretKey = kwargs.get("secretKey","")
        self.__datetime = kwargs.get("datetime","")

    @property
    def apiKey(self):
        return self.__apiKey

    @apiKey.setter
    def apiKey(self,value):
        self.__apiKey = value

    @property
    def secretKey(self):
        return self.__secretKey 

    @secretKey.setter
    def secretKey(self,value):
        self.__secretKey = value

    @property
    def datetime(self):
        return self.__datetime 
    
    @datetime.setter
    def secretKey(self,value):
        self.__datetime = value

    
    @property
    def RefreshToken(self) :
        return self.__refreshToken

    @RefreshToken.setter
    def RefreshToken(self,value):
        self.__refreshToken = value

    @property
    def AccessToken(self) :
        return self.__accessToken

    @AccessToken.setter
    def AccessToken(self,value):
        self.__accessToken = value        


