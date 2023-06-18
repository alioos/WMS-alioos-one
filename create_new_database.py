import mysql.connector


# konfiguracja połączenia z bazą danych
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="slabehaslo",
    database="out_users",
)

# utworzenie tabeli w bazie danych
cursor = db.cursor()

def create():
    #cursor.execute("CREATE DATABASE out_users")
    CREATE_TABLE = """CREATE TABLE users (users_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
    cursor.execute(CREATE_TABLE)
    print(CREATE_TABLE)


create()







