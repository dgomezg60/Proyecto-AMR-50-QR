from datetime import datetime
import elasticsearch
from Logging.ELKConection import ElasticConection
from Logging.Logging import Logging

class ElasticClass(ElasticConection):
    def __init__(self):
        super().__init__()

    def CreateIndex(self,Name):
        self.User.indices.create(index= Name)

    def SearchIndex(self,Name):
        try:
            return self.User.search(index= Name)
        except elasticsearch.NotFoundError:
            return None
        
    def GetAliasIndex(self,Name):
        try:
            return list(self.User.indices.get_alias(index= Name).keys())
        except elasticsearch.NotFoundError:
            return None
        
    def DeleteIndex(self,Name):
        _ = self.User.indices.delete(index=Name)
    
    def IngestDocuments(self,Index,Document):
        self.User.index(index=Index,document=Document)
        self.User.indices.refresh(index= Index)
    
    def SearchDocument(self,Index,Parameter):
        query = {
            "query": {
            "match": Parameter}
            }
        return self.User.search(index=Index,body=query)['hits']['hits']

    def DeleteDocuments(self,Index,Id):
        self.User.delete(index= Index,id= Id)
        self.User.indices.refresh(index= Index)
    
    def UpdateDocuments(self,Document,Value):
        for Key in Value:
            Document['_source'][f'{Key}'] = Value[f'{Key}']
        self.User.update(index=Document['_index'],id=Document['_id'],doc=Document['_source'])
        self.User.indices.refresh(index=Document['_index'])

class ElasticLogs(Logging):
    def __init__(self):
        super().__init__()

    def __GetMessaggeBase(self):
        MesaggeBase = {
            'Type': '',
            'Datetime': datetime.now().strftime("%d/%m/%Y_%H:%M:%S"),
            'RobotId': ''
        }
        return MesaggeBase

    def Debug(self,message):
        self.WDebug(message)
    
    def Info(self,message):
        LogMessage = self.__GetMessaggeBase()
        LogMessage['Type'] = 'INFO'
        LogMessage['RobotId'] = str(message['IDRobot'])
        LogMessage['Velocity'] = message['Speed']
        LogMessage['Battery'] = message['BatteryLevel']

        LogMessage.pop('Type')
        self.WInfo(LogMessage)
    
    def Warning(self,message):
        self.WWarning(message)
    
    def Error(self,message):
        LogMessage = self.__GetMessaggeBase()
        LogMessage['Type'] = 'ERROR'
        LogMessage['RobotId'] = str(message['IDRobot'])
        LogMessage['ErrorType'] = message['ErrorStatus']
        
        LogMessage.pop('Type')
        self.WError(LogMessage)
    
    def Critical(self,message):
        self.WCritical(message)