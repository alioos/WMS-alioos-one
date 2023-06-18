import MySQLdb
from flask import render_template, request, redirect, url_for, Flask, Blueprint
from app.models.zostaw.zostaw_produkt import zostaw_produkt

from app.baza_danych import baza_danych # Import modułu baza_danych


sprawdz_produkt_blueprint = Blueprint('sprawdz_produkt', __name__) # Utworzenie obiektu typu Blueprint

@sprawdz_produkt_blueprint.route('/sprawdz/produkt', methods=['GET', 'POST']) # Dekorator Blueprint
def sprawdz_produkt():
    db = baza_danych() # Utworzenie połączenia z bazą danych
    cur = db.cursor() # Utworzenie kursora
    message = "" # Zmienna przechowująca komunikat dla użytkownika

    if request.method == 'POST': # Jeśli użytkownik wysłał formularz
        nazwa = request.form['nazwa_produktu'] # Pobranie nazwy produktu z formularza
        barcode = request.form['barcode_produktu'] # Pobranie kodu kreskowego produktu z formularza
        if not nazwa and not barcode:  # Żadne pole nie zostało wypełnione
            message = "Wpisz nazwę lub kod kreskowy produktu" # Ustawienie komunikatu dla użytkownika
        else:
            cur.execute("SELECT * FROM produkty_testy WHERE nazwa = %s OR barcode = %s", (nazwa, barcode)) # Wyszukanie produktu w bazie danych
            produkt = cur.fetchone() # Pobranie wyniku zapytania
            if produkt: # Jeśli produkt został znaleziony
                print(f"Znaleziono produkt: {produkt[1]}") # Wyświetlenie nazwy produktu w konsoli
                return redirect(url_for('zostaw_produkt.zostaw_produkt', nazwa=produkt[1], barcode=produkt[2])) # Przekierowanie do widoku zostaw_produkt
            else:
                if nazwa or barcode:
                    if nazwa and barcode:
                        message = f"Nie znaleziono takiego produktu o nazwie: {nazwa} i kodzie kreskowym: {barcode}, \ndodaj go najpierw do bazy danych."
                    elif nazwa:
                        message = f"Nie znaleziono takiego produktu o nazwie: {nazwa}, dodaj go najpierw do bazy danych."
                    elif barcode:
                        message = f"Nie znaleziono takiego produktu o kodzie kreskowym: {barcode}, dodaj go najpierw do bazy danych."

    return render_template('sprawdz_produkt.html', message=message) # Wyświetlenie widoku sprawdz_produkt.html

