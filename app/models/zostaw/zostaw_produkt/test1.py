import traceback

from flask import render_template, request, redirect, url_for, Flask, Blueprint, jsonify

from app.baza_danych import baza_danych

zostaw_produkt_blueprint = Blueprint('zostaw_produkt', __name__) # Utworzenie obiektu typu Blueprint

@zostaw_produkt_blueprint.route('/zostaw/produkt/<nazwa>/<barcode>', methods=['GET', 'POST']) # Dekorator Blueprint
def zostaw_produkt(nazwa, barcode):
    message = "" # Zmienna przechowująca komunikat
    spaced_message = ""
    db = baza_danych() # Utworzenie połączenia z bazą danych
    cur = db.cursor() # Utworzenie kursora
    cur.execute("SELECT * FROM produkty_testy WHERE nazwa = %s OR barcode = %s", (nazwa, barcode)) # Wykonanie zapytania
    produkt = cur.fetchone() # Pobranie wyników zapytania
    # Pobranie wszystkich opakowań zbiorczyc, wszystkich miejsc, w których znajduje się dany produkt + ilość produktu w opakowaniu, danym miejscu
    query = ''' 
        SELECT barcode_opak, barcode_miejsce, SUM(1) AS ilość
        FROM przypisane_testy
        WHERE nazwa_produktu = %s AND barcode_produktu = %s
        GROUP BY barcode_opak, barcode_miejsce
        ORDER BY barcode_opak
    '''
    # Wykonanie zapytania
    cur.execute(query, (nazwa, barcode))
    miejsca = cur.fetchall()
    # Jeżeli produkt nie istnieje w bazie danych
    if request.method == 'POST':
        message = ""
        # Pobranie danych z formularza
        nazwa_opakowania = request.form.get('opakowanie_zbiorcze')
        nazwa_miejsca = request.form.get('miejsce')

        if not nazwa_opakowania or not nazwa_miejsca:
            message = '''1. Wpisz tylko opakowanie, jeżeli istnieje i jest już przypisane do miejsca(nie ma potrzeby wpisywania miejsca)\n
            2. Wpisz tylko miejsce, jeżeli chcesz przypisać produkt bez opakowania\n
            3. Wpisz opakowanie i miejsce, jeżeli chcesz przypisać produkt do opakowania i miejsca'''

            return render_template('zostaw_produkt.html', produkt=produkt, miejsca=miejsca, message=message)

        else:
            cur.execute("SELECT * FROM opak_zbiorcze_testy WHERE nazwa = %s", (nazwa_opakowania,))
            opakowanie = cur.fetchone()
            cur.execute("SELECT * FROM miejsca_testy WHERE nazwa = %s", (nazwa_miejsca,))
            miejsce = cur.fetchone()
            if opakowanie is not None and miejsce is not None: # Jeżeli opakowanie i miejsce istnieją w bazie danych
                # Sprawdzenie czy opakowanie już istnieje w przypisane_testy z innym barcode_miejsce
                cur.execute("SELECT barcode_miejsce FROM przypisane_testy WHERE barcode_opak = %s AND nazwa_produktu = %s", (nazwa_opakowania, nazwa))
                existing_barcode_miejsce = cur.fetchone()

                if existing_barcode_miejsce and existing_barcode_miejsce[0] != nazwa_miejsca:
                    message = f"Opakowanie zbiorcze: {nazwa_opakowania } znajduje się już na miejscu: {existing_barcode_miejsce[0]}"
                else:
                    cur.execute(
                        "INSERT INTO przypisane_testy (nazwa_produktu, barcode_produktu, barcode_opak, barcode_miejsce, data_przypisania) VALUES (%s, %s, %s, %s, NOW())",
                        (nazwa, barcode, nazwa_opakowania, nazwa_miejsca))
                    db.commit()
                    message = "Produkt został dodany do istniejących wpisów o przypisaniu do opakowania i miejsca."
                    return redirect(url_for('zostaw_produkt.zapisany_produkt', nazwa=nazwa, barcode=barcode, message=message))
            else:
                if opakowanie is None and miejsce is None:
                    message = "Nie znaleziono takiego opakowania : " + nazwa_opakowania + " i takiego miejsca : " + nazwa_miejsca + ", dodaj je do bazy danych."
                elif miejsce is None:
                    message = "Nie znaleziono takiego miejsca : " + nazwa_miejsca + ", dodaj je do bazy danych."
                elif opakowanie is None:
                    message = "Nie znaleziono takiego opakowania : " + nazwa_opakowania + ", dodaj je do bazy danych."

    return render_template('zostaw_produkt.html', produkt=produkt, miejsca=miejsca, message=message)


@zostaw_produkt_blueprint.route('/zapisany_produkt/<nazwa>/<barcode>', methods=['GET'])
def zapisany_produkt(nazwa, barcode):
    message = request.args.get('message')  # Pobranie komunikatu z parametrów URL
    db = baza_danych()
    cur = db.cursor()
    cur.execute("SELECT * FROM przypisane_testy ORDER BY id DESC LIMIT 1") # Wykonanie zapytania
    przypisane = cur.fetchall()
    db.close()
    return render_template('zapisany_produkt.html', nazwa=nazwa, barcode=barcode, message=message, przypisane=przypisane)




