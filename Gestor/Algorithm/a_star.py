from pprint import pprint
import numpy as np
from DB.SQLLite import DB

class Map:
    def __init__(self):
        self.Map = {}
        self.__Db = DB()
        self.__Db.Connect()
        self.__FormMap()
    
    def __FormMap(self):
        Table = self.__Db.ReadTable('Map')
        for Row in Table:
            Relations = self.__Db.Find('NEIGHBOURDS',"Next == '{}'".format(Row[0]))
            Neighbours = []
            for Neighbour in Relations:
                Weight = self.__Db.Find('SEPARATION',f'IDdistance == {Neighbour[-1]}')[0]
                NeighbourData = {'Node': Neighbour[0],'Weight': Weight[-1]}
                Neighbours.append(NeighbourData)
            self.Map[f'{Row[0]}'] = {'Coordenates':[Row[1],Row[2]],'neighbours':Neighbours}

class AStar(Map):
  def __init__(self):
       super().__init__()
       self.Graph = self.Map
  
  def __CalculateDistance(self,StartPoint,Endpoint,Weight):
    return np.sqrt(pow((StartPoint[0]-Endpoint[0]),2)+pow((StartPoint[1]-Endpoint[1]),2))*Weight

  def Search(self,Start,End):
    Path = []
    Path.append(Start)
    StartPoint = self.Graph[f'{Start}']
    EndPoint = self.Graph[f'{End}']
    while True:
        Distances = []
        for edge in StartPoint['neighbours']:
            Distances.append(self.__CalculateDistance(self.Graph['{}'.format(edge['Node'])]['Coordenates'],EndPoint['Coordenates'],edge['Weight']))
        MinDistance = min(Distances)
        NextPoint = StartPoint['neighbours'][Distances.index(MinDistance)]['Node']
        Path.append(NextPoint)
        if NextPoint == End:
            break
        else:
            StartPoint = self.Graph[f'{NextPoint}']
    return Path,len(Path)