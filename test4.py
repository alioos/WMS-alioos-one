import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="slabehaslo",
    database="projekt_szafa",
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE our_users")

mycursor.execute("SHOW DATABASES")
for db in mycursor:
    print(db)

