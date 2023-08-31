import asyncio
from .ClientClass import main
import websockets

def origin():
    robot = AMR(0)
    robot.NewAMR()

class AMR:
    def __init__(self,id):
        self.id = id
        self.Status = 'Enty'
        self.Battery = 0
        self.Position = 'A0'
        self.Path = ''

    def WebsocketClient(self):
        try:
            print('Inicio cliente')
            asyncio.run(main(self.id,"59"))
        except websockets.exceptions.ConnectionClosedError:
            print("Server turn off")
        except:
            print("Server turn off")

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
        self.WebsocketClient()
