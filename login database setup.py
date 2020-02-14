import sqlite3

login = sqlite3.connect("login.db")

try:
    login.execute("""CREATE TABLE LOGIN
                (ID USERNAME    TEXT    NOT NULL,
                PASSWORD        TEXT    NOT NULL)""")
    
except sqlite3.OperationalError:
    print("table LOGIN exists")

c = login.cursor()

