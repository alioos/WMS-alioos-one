import MySQLdb
from flask import Flask, render_template, request

from app.models.zostaw.zostaw_opak_zbiorcze.sprawdz_opak_zbiorcze.sprawdz_opak_zbiorcze import sprawdz_opak_zbiorcze_blueprint
from app.models.zostaw.zostaw_opak_zbiorcze.zostaw_opak_zbiorcze import zostaw_opak_zbiorcze_blueprint
from app.models.zostaw.zostaw_produkt.sprawdz_produkt.sprawdz_produkt import sprawdz_produkt_blueprint
from app.models.zostaw.zostaw_produkt.zostaw_produkt import zostaw_produkt_blueprint
from baza_danych import baza_danych



app = Flask(__name__)


@app.route('/')
def index2():
    return render_template('index2.html')



app.register_blueprint(sprawdz_produkt_blueprint) # Rejestracja Blueprint sprawdz_produkt_blueprint

app.register_blueprint(zostaw_produkt_blueprint) # Rejestracja Blueprint zostaw_produkt_blueprint

app.register_blueprint(sprawdz_opak_zbiorcze_blueprint) # Rejestracja Blueprint sprawdz_opak_zbiorcze_blueprint

app.register_blueprint(zostaw_opak_zbiorcze_blueprint) # Rejestracja Blueprint sprawdz_opak_zbiorcze_blueprint

#@app.route('/sprawdz/produkt')
#def do_sprawdz_produkt():
    #return sprawdz_produkt()



@app.route('/us', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get the form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        db = baza_danych()
        cur = db.cursor()
        cur.execute("INSERT INTO users(name, email) VALUES (%s, %s)", (name, email))
        db.commit()
        cur.close()
        return 'success'
    return render_template('index.html')


@app.route('/users')
def users():
    db = baza_danych()
    cur = db.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)


if __name__ == '__main__':
    app.run(host='192.168.1.7', port=5001, debug=True)




