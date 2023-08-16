from DB.SQLLite import DB
# from pprint import pprint
# from SQLLite import DB

def Graphs():
    DataBase = DB()
    DataBase.Connect()
    Map = DataBase.ReadTableSimple('MAP','NEIGHBOURDS','IDPosition','Next')
    GraphList = {}
    for node in Map:  
        if node[0] in GraphList:
            Distance = DataBase.Find('SEPARATION','IDdistance={}'.format(node[4]))[0]
            GraphList[node[0]]['Edge'].append({'neightbour':'{}'.format(node[6]),'weight':'{}'.format(Distance[1])})
        else:
            Graph_data = {}
            Distance = DataBase.Find('SEPARATION','IDdistance={}'.format(node[4]))[0]
            Graph_data['Node'] = node[0]
            Graph_data['Position'] = [node[1],node[2]]
            Graph_data['Status'] = node[3]
            Graph_data['Edge'] = [{'neightbour':'{}'.format(node[6]),'weight':'{}'.format(Distance[1])}]
            GraphList['{}'.format(node[0])] = Graph_data
    return GraphList