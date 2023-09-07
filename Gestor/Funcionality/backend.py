import asyncio
import random
import time
from Algorithm.a_star import AStar
from DB.SQLLite import DB
from Logging.ElasticCluster import ElasticLogs
from WebsocketServer.LaunchServer import Server
from Algorithm.a_star import AStar

class back:
    def __init__(self):
        self.ServerP = Server()
        time.sleep(0.5)
        self.Db = DB()
        self.__ElasticLogs = ElasticLogs()
        self.Db.Connect()
        asyncio.run(self.InitCicle())
        
    async def InitCicle(self):
        print('What robot do you want to move? \n Id = 0')
        self.IdRobot = 0
       
        print('What point do you want to send the robot?')
        Positions = self.Db.ReadColum('Map','IDPosition')
        self.EndPoint = random.choice(Positions)[0]
        #self.EndPoint = input()
        if self.Db.Find('Map',f"IDPosition == '{self.EndPoint}'"):
            _ = input()
            #try:
            await asyncio.create_task(self.SendPath(self.IdRobot,self.EndPoint))
            # except KeyError:
            #     print('Dont have AMR with this ID')
        else:
            print('This position doesnt exist')
        print('Another cicle, press enter')
        _ = input()
        await self.InitCicle()
        
    async def SendPath(self,Id,EndPoint):
        AMRData = self.Db.Find('AMR',f'IDAMR == {Id}')
        StartPoint = AMRData[0][2]
        self.Path,self.PathLenght = AStar().Search(StartPoint,EndPoint)
        StringPath = ' '.join(e for e in self.Path)
        print(f'Path --------> {self.Path}')
        if self.PathLenght > 1:
            self.Db.UpdateDate('AMR',f"Path == '{StringPath}'",f'IDAMR == {self.IdRobot}')
            for Point in self.Path[1:]:
                Position = self.Db.Find('MAP',f"IDPosition == '{Point}'")[0]
                await self.ServerP.send_message(Id,[Position[1],Position[2],0])
                ChangePosition = True
                while ChangePosition:
                    ChangePosition = await self.ReadP(Id,Point)
            self.Db.UpdateDate('AMR',f"Path == ''",f'IDAMR == {self.IdRobot}')

    async def ReadP(self,Id,DestinyPoint):
        MessageData = await self.ServerP.read_message(Id) 
        MessageData['Position'] = self.__NormalicePosition(MessageData['Position'])
        print(f'From Robot {Id} recibed {MessageData}')
        if MessageData['ErrorStatus'] == 0:
            self.__ElasticLogs.Info(MessageData)
        else:
            self.__ElasticLogs.Error(MessageData)
        IdPosition = self.Db.Find('MAP',f"XPosition == {MessageData['Position'][0]} AND YPosition == {MessageData['Position'][1]}")[0]
        if IdPosition[0] == DestinyPoint:
            self.Db.UpdateDate('AMR',f"Position == '{IdPosition[0]}'",f'IDAMR == {self.IdRobot}')
            return False
        return True

    def __NormalicePosition(self,PositionString):
        try:
            Position = PositionString[1:-1]
            return Position.split(',')
        except AttributeError:
            return PositionString