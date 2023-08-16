import asyncio
from threading import Thread
import websockets
import json

class client():
    def __init__(self,Identify):
        self.Id = Identify
        self.Ip = '192.168.1.171'
        self.Ports = [8765,8766]
        self.Position = [0,0,0]
         
    async def connected(self,Token):   
        try:
            self.__clientListener = await websockets.connect(f'ws://{self.Ip}:{self.Ports[0]}')
            self.__clientSender = await websockets.connect(f'ws://{self.Ip}:{self.Ports[1]}')
            self.token = Token
            await self.__SendAuthenticationMessage()
        except websockets.exceptions.ConnectionClosedError:
            print("\nConnection Error")
        except KeyboardInterrupt:
            print("\nDisconnect")

    async def __SendAuthenticationMessage(self):
        struct = r'{{"Token":"{}","ID":"{}"}}'
        FirstMessage = struct.format(self.token,self.Id)
        await asyncio.gather(self.__clientSender.send(FirstMessage),self.__clientListener.send(FirstMessage))

    #async def SendParameters(self,Position,Speed,Blocked,Queued,Status,ErrorStatus,BatteryLevel):
    async def SendParameters(self):
            struct = r'{{"IDRobot":"{}","Position":"{}","Speed":50,"Blocked":true,"Queued":true,"Status":"Enty","ErrorStatus":0,"BatteryLevel":20}}'
            #struct  = r'{{"IDRobot":"{}","Position":"{}","Speed":"{}","Blocked":"{}","Queued":"{}","Status":"{}","ErrorStatus":"{}","BatteryLevel":"{}"}}'
            #message = struct.format(self.Id,Position,Speed,Blocked,Queued,Status,ErrorStatus,BatteryLevel)
            message = struct.format(self.Id,self.Position)
            await self.__clientSender.send(message)
            await asyncio.sleep(1)

    async def ListeningServer(self):
        Order = await self.__clientListener.recv()
        if Order != 'OK':
            self.message = json.loads(Order)
            #print("ID:{}, Position: {}".format(self.message['IDRobot'],self.message['Position']))
            self.Position = self.message['Position']
            await self.SendParameters()
        await self.ListeningServer()

async def main(id,token):
    Amr = client(id)
    await Amr.connected(token)
    try:
        await asyncio.gather(Amr.ListeningServer(),Amr.SendParameters())
    except KeyboardInterrupt:
        print('Disconnect')
        quit()
    except websockets.exceptions.ConnectionClosedError:
         print('Unathenticated')

if __name__ == '__main__':
    Ip = '192.168.1.171'
    Ports = [8765,8766]
    asyncio.run(main(0,'59'))


