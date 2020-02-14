import sqlite3


login = sqlite3.connect("login.db")
try:
    login.execute("""CREATE TABLE LOGIN
                (ID USERNAME    TEXT    NOT NULL,
                PASSWORD        TEXT    NOT NULL)""")
    
except sqlite3.OperationalError:
    print("table LOGIN exists")



preset = sqlite3.connect("preset.db")
try:
    preset.execute("""CREATE TABLE PRESET
                (ID PRIMARY KEY INT     NOT NULL,
                SIMNAME         TEXT    NOT NULL,
                AMPLITUDE       FLOAT   NOT NULL,
                MASS            FLOAT   NOT NULL,
                SPRING_CONST    FLOAT   NOT NULL)""")
    
except sqlite3.OperationalError:
    print("table PRESET exists")


d = login.cursor()
c = preset.cursor()


simname = str(input()).lower()
amplitude = float(input())
mass = float(input())
spring_const = float(input())

##### HASHING THROUGH THE SNOW
##### The database will create primary ids by hashing simname

unhashedKey = 0
for x in range(0,len(simname)):
    if simname[x] != " ":
        unhashedKey = unhashedKey + (ord(simname[x])-96)
hashedKey = unhashedKey % 20

c.execute("""INSERT INTO PRESET
            (ID,SIMNAME,AMPLITUDE,MASS,SPRING_CONST)
            VALUES
            (hashedKey,simname,amplitude,mass,spring_const)""")


login.close()
preset.close()






