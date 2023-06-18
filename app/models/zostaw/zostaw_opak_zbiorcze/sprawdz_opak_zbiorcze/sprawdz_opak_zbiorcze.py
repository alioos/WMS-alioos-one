from flask import render_template, request, Blueprint, redirect, url_for
from app.baza_danych import baza_danych # Import modułu baza_danych


sprawdz_opak_zbiorcze_blueprint = Blueprint('sprawdz_opak_zbiorcze', __name__) # Utworzenie obiektu typu Blueprint


@sprawdz_opak_zbiorcze_blueprint.route('/sprawdz_opak_zbiorcze/opakowanie', methods=['GET', 'POST']) # Dekorator Blueprint
def sprawdz_opak_zbiorcze():
    db = baza_danych() # Utworzenie połączenia z bazą danych
    cur = db.cursor() # Utworzenie kursora
    message = "" # Zmienna przechowująca komunikat dla użytkownika

    if request.method == 'POST': # Jeśli użytkownik wysłał formularz
        nazwa_opakowania = request.form['nazwa_opak_zbiorcze'] # Pobranie nazwy produktu z formularza
        barcode_opakowania = request.form['barcode_opak_zbiorcze'] # Pobranie kodu kreskowego produktu z formularza
        if not nazwa_opakowania and not barcode_opakowania:  # Żadne pole nie zostało wypełnione
            message = "Wpisz nazwę lub kod kreskowy produktu"  # Ustawienie komunikatu dla użytkownika
        else:
            cur.execute("SELECT * FROM opak_zbiorcze_testy WHERE nazwa = %s OR barcode = %s",
                        (nazwa_opakowania, barcode_opakowania))  # Wyszukanie produktu w bazie danych
            opakowanie = cur.fetchone()  # Pobranie wyniku zapytania
            if opakowanie:  # Jeśli produkt został znaleziony
                print(f"Znaleziono produkt: {nazwa_opakowania}")  # Wyświetlenie nazwy produktu w konsoli
                return redirect(url_for('zostaw_opak_zbiorcze.zostaw_opak_zbiorcze', nazwa_opakowania=opakowanie[1],
                                        barcode_opakowania=opakowanie[2]))  # Przekierowanie do widoku zostaw_produkt
            else:
                if nazwa_opakowania or barcode_opakowania:
                    if nazwa_opakowania and barcode_opakowania:
                        message = f"Nie znaleziono takiego produktu o nazwie: {nazwa_opakowania} i kodzie kreskowym: {barcode_opakowania}, \ndodaj go najpierw do bazy danych."
                    elif nazwa_opakowania:
                        message = f"Nie znaleziono takiego produktu o nazwie: {nazwa_opakowania}, dodaj go najpierw do bazy danych."
                    elif barcode_opakowania:
                        message = f"Nie znaleziono takiego produktu o kodzie kreskowym: {barcode_opakowania}, dodaj go najpierw do bazy danych."

    return render_template('sprawdz_opak_zbiorcze.html', message=message) # Wyświetlenie widoku sprawdz_produkt.html