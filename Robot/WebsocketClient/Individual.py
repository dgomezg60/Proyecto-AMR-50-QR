import asyncio
import sys
try:
    from WebsocketClient.ClientClass import main
except:
    from ClientClass import main
try:
    from DB.SQLLite import DB
except:
    sys.path.insert(1, '/home/qxt-0004/Downloads/AMR-Simulator-main/')
    from DB.SQLLite import DB
import websockets

def origin():
    robot = AMR()
    robot.NewAMR()

class AMR:
    def __init__(self):
        self.DB = DB()
        self.DB.Connect()
        self.Status = 'Enty'
        self.Battery = 0
        self.Position = 'A0'
        self.Path = ''

    def WebsocketClient(self):
        try:
            asyncio.run(main(self.id,"59"))
        except websockets.exceptions.ConnectionClosedError:
            print('Server turn off')

    def GetPath(self):
        return self.Path

    def ChangeStatus(self):
        UData = f'Status={self.Status}'
        self.DB.UpdateDate('AMR',UData,f'IDAMR={self.id}')

    def ChangeBattery(self):
        UData = f'Battery={self.Battery}'
        self.DB.UpdateDate('AMR',UData,f'IDAMR={self.id}')

    def Move(self):
        if self.Path != '':
            self.__NextPoint() #Toma la path separada por comas y le quita un un punto que lo carga en position
            UData = f'Position={self.Position},Path={self.Path}'
            self.DB.UpdateDate('AMR',UData,f'IDAMR={self.id}')

    def NewAMR(self):
        self.DB.DeleteRow('AMR',f'IDAMR=0')
        LastObject = self.DB.ReadOrder('AMR','IDAMR ASC')
        try:
            self.id = int(LastObject[0][0])+1
        except TypeError:
            self.id = 0
        self.DB.InsertRow('AMR',f"({self.id},'{self.Status}','{self.Position}',{self.Battery},'{self.Path}')")
        self.WebsocketClient()

if __name__ == '__main__':
    origin()