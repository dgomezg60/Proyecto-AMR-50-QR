from Algorithm.a_star import AStar
from DB.SQLLite import DB
from WebsocketServer.Server import Server
import asyncio

def LockForPath(IDRobot,EndPoint):
    db = DB()
    db.Connect()
    Amr = db.Find('AMR',f'IDAMR={IDRobot}')
    try:
        from GUI.Grafos.main import MapGraph
    except:
        quit()
    ServerObj = Server()
    if EndPoint[0] == '[':
        Path = [EndPoint]
    if EndPoint[0] != '[':
        Algorithm = AStar(MapGraph,Amr[0][2],EndPoint)
        Path,PathLenght = Algorithm.search()
        print(Path)
    #     CoordinatePath = []
    #     for Points in Path:
    #         Coordinates = db.Find('MAP',f"IDPosition = '{Points}'")[0]
    #         Position = [Coordinates[1],Coordinates[2],0]
    #         CoordinatePath.append(Position)
    #     Path = CoordinatePath
    # db.UpdateDate('AMR',f"Path = '{Path}'",f'IDAMR={IDRobot}')
    # for Point in Path:
    #     asyncio.run(ServerObj.send_message(0,Point))
    #     asyncio.run(asyncio.sleep(1))
