import MySQLdb
from flask import Flask


def baza_danych():
    app = Flask(__name__)
    # Konfiguracja połączenia z bazą danych
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'slabehaslo'
    app.config['MYSQL_DB'] = 'projekt_szafa'

        # Utworzenie połączenia z bazą danych

    db = MySQLdb.connect(host=app.config['MYSQL_HOST'],
                        user=app.config['MYSQL_USER'],
                        passwd=app.config['MYSQL_PASSWORD'],
                        db=app.config['MYSQL_DB'])

    return db