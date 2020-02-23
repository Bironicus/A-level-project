import sqlite3
import binascii

login = sqlite3.connect("login.db")
l = login.cursor()

try:
    l.execute("""create table login (username, password)""")
    
except sqlite3.OperationalError:
    print("table login exists")


##username = str(input()).lower()
##password = input()
    
username = "io"
password = "vogon poetry 78"


### VERNAM CIPHER XOR password encryption

encryption_key = binascii.a2b_uu(binascii.b2a_uu("i"))
print(encryption_key)

##encryption_key = str(0) + bin(ord("Z"))[2:]
##print(encryption_key)
##
##encrypted_password = ""
##for x in range(0,len(password)):
##    
##    if password[x] != " ":
##        char = bin(ord(password[x]))[2:]
##        while len(char) != 8:
##            char = str(0) + char #char must be 8 bit




binary_str = 11001100
print(chr(int(binary_str,2)))

#####https://www.tutorialspoint.com/python_text_processing/python_conversion_binary_ascii.htm

