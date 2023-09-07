from WebsocketServer.LaunchServer import Server
from threading import Thread
from Funcionality.backend import back

def DefineServer():
    _ = Server()

if __name__ == '__main__':
    Thread1 = Thread(target= DefineServer)
    Thread1.start()
    _ = back()
