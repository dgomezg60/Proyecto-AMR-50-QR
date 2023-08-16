import sqlite3 as sql

class DB:
    def __init__(self):
        pass
    
    def ReadTableDouble(self,Table,SecTable,PrimaryKey,ForeignKey1,ForeignKey2):
        self.__cursor.execute(f"""SELECT * FROM {Table} 
                              INNER JOIN {SecTable} ON  {Table}.{PrimaryKey} = {SecTable}.{ForeignKey1}
                              INNER JOIN {SecTable} ON  {Table}.{PrimaryKey} = {SecTable}.{ForeignKey2}
                            """)
        Date = self.__cursor.fetchall()
        return Date

    def ReadTableSimple(self,Table,SecTable,PrimaryKey,ForeignKey):
        self.__cursor.execute(f"SELECT * FROM {Table} INNER JOIN {SecTable} ON  {Table}.{PrimaryKey} = {SecTable}.{ForeignKey}")
        Date = self.__cursor.fetchall()
        return Date
    
    def ReadTable(self,Table):
        self.__cursor.execute(f"SELECT * FROM {Table}")
        Date = self.__cursor.fetchall()
        return Date 

    def ReadColum(self,Table,Colum):
        Read = f'SELECT {Colum} FROM {Table}'
        self.__cursor.execute(Read)
        IDs = self.__cursor.fetchall()
        return IDs

    def DeleteRow(self,Table,Condition):
        Delete = f"DELETE FROM {Table} WHERE {Condition}"
        self.__cursor.execute(Delete)
        self.__conn.commit()

    def UpdateDate(self,Table,UpdateData,Objective):
        Update = f"UPDATE {Table} SET {UpdateData} WHERE {Objective}"
        self.__cursor.execute(Update)
        self.__conn.commit()


    def Find(self,Table,Condition):
        LockFor = f"SELECT * FROM {Table} WHERE {Condition}"
        self.__cursor.execute(LockFor)
        Data = self.__cursor.fetchall()
        return Data

    def ReadOrder(self,Table,Field):
        insert = f"SELECT * FROM {Table} ORDER BY {Field}"
        self.__cursor.execute(insert)
        Data = self.__cursor.fetchall()
        print(Data)

    def CreateTable(self):
        self.__cursor.execute("""CREATE TABLE MAP (IDPosition TEXT PRIMARY KEY, 
                                                    XPosition INTEGER,
                                                    YPosition TEXT,
                                                    Status INTEGER) """)
        self.__cursor.execute("""CREATE TABLE NEIGHBOURDS (IDNeighbourd INTEGER PRIMARY KEY, 
                                                    Next TEXT NOT NULL,
                                                    Neighbourd TEXT NOT NULL,
                                                    FOREIGN KEY(Next) REFERENCES MAP(IDPosition),
                                                    FOREIGN KEY(Neighbourd) REFERENCES MAP(IDPosition) ) """)
        self.__cursor.execute("""CREATE TABLE SEPARATION (IDdistance INTEGER PRIMARY KEY, 
                                                    Distance INTEGER NOT NULL,
                                                    FOREIGN KEY(IDdistance) REFERENCES NEIGHBOURDS(IDNeighbourd) )""")
        self.__cursor.execute("""CREATE TABLE AMR (IDAMR TEXT, 
                                                    Status INTEGER NOT NULL,
                                                    Position TEXT NOT NULL PRIMARY KEY,
                                                    Battery INTEGER NOT NULL,
                                                    Path TEXT NULL,
                                                    FOREIGN KEY(Position) REFERENCES MAP(IDPosition) ) """)
        self.__conn.commit()

    def InsertRow(self,Table,Value):
        Insert = f"INSERT INTO {Table} VALUES {Value}"
        self.__cursor.execute(Insert)
        self.__conn.commit()

    def Connect(self):
        self.__conn = sql.connect("DB/db/Probe_sql.db")
        self.__conn.commit()
        self.__cursor = self.__conn.cursor()

    def Disconnect(self):
        self.__conn.commit()
        self.__conn.close()

# if __name__ == '__main__':
#     DataBase = DB()
#     DataBase.Connect()
#     DataBase.UpdateDate("SEPARATION",f"Distance = {5}",f"IDdistance = {0}")