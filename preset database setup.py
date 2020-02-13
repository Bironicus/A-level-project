import sqlite3

preset = sqlite3.connect("preset.db")

try:
    preset.execute("""CREATE TABLE PRESET
                (ID INT PRIMARY KEY     NOT NULL,
                SIMNAME         TEXT    NOT NULL,
                AMPLITUDE       FLOAT   NOT NULL,
                MASS            FLOAT   NOT NULL,
                SPRING_CONST    FLOAT   NOT NULL)""")
except sqlite3.OperationalError:
    print("table PRESET exists")

c = preset.cursor()


##### HASHING THROUGH THE SNOW
##### The database will create primary ids by hashing simname

simname = str(input()).lower()

unhashedKey = 0
for x in range(0,len(simname)):
    unhashedKey = unhashedKey + (ord(simname[x])-96)
hashedKey = unhashedKey % 20





preset.close()
