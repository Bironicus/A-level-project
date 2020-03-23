import sqlite3


def create_table(db_name,table_name,sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("drop table if exists {0}".format(table_name))
        cursor.execute("select name from sqlite_master where name = ?",(table_name,))
        cursor.execute(sql)
        db.commit()



db_name = "UserInfo.db"

try:
    table_name = "UserInfo"
    sql = """create table Login
                        (UserID integer,
                        Username string,
                        Password string,
                        primary key (UserID))"""

    create_table(db_name,table_name,sql)
except sqlite3.OperationalError:
    print("table Login already exists")



####try:
####    db_name = "Spring.db"
####    table_name = "Spring"
####    sql = """create table Pendulums
####                        (SpringID      integer,
####                        UserID       integer,
####                        SimulationName string,
####                        Amplitude      float,
####                        Mass           float,
####                        SpringConstant float,
####                        Damping        boolean,
####                        primary key (SpringID))"""
####    create_table(db_name,table_name,sql)
####except sqlite3.OperationalError:
####    print("table Pendulums already exists")

############################
    
####springid = 1
####username = "io"
####simulationname = "test spring"
####amplitude = 1.5
####mass = 0.8
####springconstant = 1.0
####damping = False
####
####Values = (int(springid),str(username),str(simulationname),
####          float(amplitude),float(mass),float(springconstant),bool(damping))

####with sqlite3.connect(db_name) as db:
####        cursor = db.cursor()
######        sql = """insert into Pendulums(SpringID,Username,SimulationName,Amplitude,Mass,SpringConstant,Damping) values(?,?,?,?,?,?,?)"""  
####        sql = """insert into Pendulums values(?,?,?,?,?,?,?)"""
####        cursor.execute(sql,Values)
####        db.commit()
####        quit()

userid = 1
username = "bim"
password = "gordons alive"
Values = (int(userid),str(username),str(password))

with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql = """insert into Login(UserID,Username,Password) values(?,?,?)"""
        cursor.execute(sql,Values)
        db.commit()
        quit()

