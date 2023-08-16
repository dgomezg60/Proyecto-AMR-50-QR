import asyncio
from threading import Thread
import websockets
import json

from DB.SQLLite import DB


class Server(object):
    __instance = None

    async def authenticate(self,FirstMessage,client,typ):
        message = json.loads(FirstMessage)
        if message['Token'] == "59":
            authenticated = True
            if typ == 1:
                self.ClientAuthorisedListener[message['ID']] = client
            if typ == 2:
                self.ClientAuthorisedSender[message['ID']] = client
        else:
            authenticated = False
        if authenticated:
            return True
        else:
            return False

    async def disconect(self,client):
        await client.close()
        print(f'Client disconected {client.id}')
        try:
            _ = self.ClientAuthorisedSender.pop(list(self.ClientAuthorisedSender.keys())[list(self.ClientAuthorisedSender.values()).index(client)])
            _ = self.ClientAuthorisedListener.pop(list(self.ClientAuthorisedListener.keys())[list(self.ClientAuthorisedListener.values()).index(client)])
        except ValueError:
            pass

    ##-------------------------------------------------------------------Server listen----------------------------------------------------------------------------------------------
    ##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def read_message(self,client):
        text = await client.recv()
        message = json.loads(text)
        print("Server Read: ID:{}, Position: {}".format(message['IDRobot'],message['Position']))
        IdPosition = self.__DB.Find('MAP','XPosition = {} AND YPosition = {}'.format(message['Position'][1],message['Position'][4]))
        self.__DB.UpdateDate('AMR',f"Position = '{IdPosition[0][0]}'",f"IDAMR = {message['IDRobot']}")
        await self.read_message(client)

    async def server_handler_listen(self,client):
        authenticated = False
        auth_message = await client.recv()
        authenticated = await self.authenticate(auth_message,client,1)
        if authenticated:
            try:
                print(f'Client conected {client.id} to Listening Server')
                await self.read_message(client)
            except websockets.exceptions.ConnectionClosed:
                await self.disconect(client)
        else:
            await client.close()

    ##-------------------------------------------------------------------Server send----------------------------------------------------------------------------------------------
    ##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def send_message(self,Id,position):
        try:
            client = self.ClientAuthorisedSender[f'{Id}']
            if position != None:
                struct = r'{{"IDRobot":"{}","Position":"{}"}}'
                message = struct.format(Id,position)
                print('Envio mensaje a Id {}, mensaje:{}'.format(Id,message))
                await client.send(message)
            else:
                await client.send('OK')
                
        except KeyError:
            print(f'Cliend with ID {Id} doesnt exist')
        except websockets.exceptions.ConnectionClosedOK:
            print(f'Client with ID {Id} disconnect')

    async def server_handler_send(self,client):
        authenticated = False
        auth_message = await client.recv()
        authenticated = await self.authenticate(auth_message,client,2)  
        if authenticated:
            print(f'Client conected {client.id} to Sender Server')
            try:
                while len(self.ClientAuthorisedSender) != 0:
                    await asyncio.sleep(10)
                    for client in self.ClientAuthorisedSender:
                        await self.send_message(client,None)
            except websockets.exceptions.ConnectionClosed:
                await self.disconect(client)
        else:
            await client.close()

    ##------------------------------------------------------------------- Start Server ----------------------------------------------------------------------------------------------
    ##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def WaitClosed(self,server):
        await server.wait_closed()

    async def start_server(self):
        self.__DB = DB()
        self.__DB.Connect()
        ListeningServer = await websockets.serve(self.server_handler_listen,self.Ip, self.Ports[1])
        print(f'Listening server turn on, at {self.Ip}:{self.Ports[1]}')
        SendingServer = await websockets.serve(self.server_handler_send, self.Ip, self.Ports[0])
        print(f'Sending server turn on, at {self.Ip}:{self.Ports[0]}')
        await asyncio.gather(self.WaitClosed(ListeningServer),self.WaitClosed(SendingServer))

    ##------------------------------------------------------------------- Singleton ----------------------------------------------------------------------------------------------
    ##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Server,cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if(self.__initialized): return
        self.__initialized = True
        self.ClientAuthorisedListener = {}
        self.ClientAuthorisedSender = {}
        self.Ports = [8765,8766]
        self.Ip = '192.168.1.171'
        try:
            asyncio.run(self.start_server())
        except KeyboardInterrupt:
            print('\nServer turn off')
        except TimeoutError:
            print('\nDisconect out of time')

def main():
    ServerObj = Server()
    
# if __name__ == '__main__':
#     ServerObj = Server()