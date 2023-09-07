from datetime import datetime
import logging
import os
import time

class Logging():
    def __init__(self):
        self.tam = 0
        self.Log = logging
        #self.__LogsDirPath ="Logging\\Logs"
        # try:
        #     self.__LastLogFile = os.listdir(self.__LogsDirPath)[-1]
        #     self.__PathLogFile = self.__LogsDirPath+"\\"+self.__LastLogFile
        #     self.__FileHandler = False
        #     self.__PathLogFile = self.__SizeOf()
        # except IndexError:
        self.__PathLogFile = self.__CreateNewLogFile()
        self.__ConfigurationLog()
    
    def __ConfigurationLog(self):
        self.__Logger = self.Log.getLogger()
        self.__Logger.setLevel(self.Log.INFO)
        #self.__PathLogFile = self.__SizeOf()
        if len(self.__Logger.handlers) == 0:
            self.__FileHandler = self.Log.FileHandler(self.__PathLogFile)
            self.__FileHandler.setLevel(self.Log.INFO)
            Format = self.Log.Formatter('%(levelname)s - %(asctime)s - %(threadName)s- %(processName)s - %(message)s')
            self.__FileHandler.setFormatter(Format)
            self.__Logger.addHandler(self.__FileHandler)

    def __SizeOf(self):
        if os.path.getsize(self.__PathLogFile) >= 1024*10:
            if self.__FileHandler:
                self.__Logger.removeHandler(self.__FileHandler)
                self.__FileHandler.close()      
            self.__PathLogFile = self.__CreateNewLogFile()
        return self.__PathLogFile

    def __CreateNewLogFile(self):
        current_datetime = datetime.now()
        try:
            _ = open(f'Logging\\Logs\\log_{current_datetime.strftime("%d-%m-%Y")}.log','x').close()
        except FileExistsError:
            pass
        return f'Logging\\Logs\\log_{current_datetime.strftime("%d-%m-%Y")}.log'
    
    def __FormText(self,message):
        text = ' '
        print(message.values())
        for data in message.values():
            text = text + f'{data}' + ' - '
        return text[:-2]

    def WDebug(self,message):
        text = self.__FormText(message)
        self.Log.debug(text)
        self.__ConfigurationLog()
    
    def WInfo(self,message):
        text = self.__FormText(message)
        self.Log.info(text)
        self.__ConfigurationLog()
    
    def WWarning(self,message):
        text = self.__FormText(message)
        self.Log.warning(text)
        self.__ConfigurationLog()
    
    def WError(self,message):
        text = self.__FormText(message)
        self.Log.error(text)
        self.__ConfigurationLog()
    
    def WCritical(self,message):
        text = self.__FormText(message)
        self.Log.critical(text)
        self.__ConfigurationLog()

# if __name__ == '__main__':
#     Log = Logging()
#     try:
#         while True:
#             Log.WDebug('Prueba de debug')
#             print('Creo Log')
#             time.sleep(0.2)
#     except KeyboardInterrupt:
#         pass