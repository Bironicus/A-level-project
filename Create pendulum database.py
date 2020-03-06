import sqlite3

def create_table(db_name,table_name,sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("drop table if exists {0}".format(table_name))
        cursor.execute("select name from sqlite_master where name = ?",(table_name,))
        cursor.execute(sql)
        db.commit()
        quit()

def create_table_sql(): #database settings
    db_name = "Pendulum.db"
    sql = """create table PendulumOptions
(SimulationID integer,
SimulationName string,
Angle integer,
Length float,
Mass integer,
primary key(SimulationID))"""
    create_table(db_name,"Pendulum",sql)

#main
create_table_sql()
