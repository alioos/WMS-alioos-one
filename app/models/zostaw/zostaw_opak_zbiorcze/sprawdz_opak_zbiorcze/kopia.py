from flask import render_template, request, redirect, url_for, Blueprint
from app.baza_danych import baza_danych

zostaw_opak_zbiorcze_blueprint = Blueprint('zostaw_opak_zbiorcze', __name__) # Utworzenie obiektu typu Blueprint

@zostaw_opak_zbiorcze_blueprint.route('/zostaw/opak_zbiorcze/<nazwa_opakowania>/<barcode_opakowania>', methods=['GET', 'POST']) # Dekorator Blueprint
def zostaw_opak_zbiorcze(nazwa_opakowania, barcode_opakowania):
    message = ""  # Zmienna przechowująca komunikat
    db = baza_danych()  # Utworzenie połączenia z bazą danych
    cur = db.cursor()  # Utworzenie kursora
    cur.execute("SELECT id_opak_zbiorcze, nazwa, barcode FROM opak_zbiorcze_testy WHERE nazwa = %s OR barcode = %s",
                (nazwa_opakowania, barcode_opakowania))
    opakowanie = cur.fetchall()
    # Jeżeli produkt nie istnieje w bazie danych
    if request.method == 'POST':
        # Pobranie danych z formularza
        opakowanie_parent = request.form.get('opakowanie_zbiorcze')
        nazwa_miejsca = request.form.get('miejsce')

        if not opakowanie_parent and not nazwa_miejsca:  # Przypadek 1: Nie wprowadzono nazwy opakowania i nazwy miejsca
            message = '''1. Wpisz opakowanie, jeżeli chcesz włożyć je do innego opakowania\n
                        2. Wpisz tylko miejsce, jeżeli chcesz przypisać opakowanie bez dodatkowego opakowania\n
                        '''
        else:
            if opakowanie_parent:  # Przypadek 1: Wprowadzono nazwę opakowania i nazwę miejsca
                cur.execute("SELECT * FROM opak_zbiorcze_testy WHERE nazwa = %s", (opakowanie_parent, ))
                opakowanie = cur.fetchone()
                cur.execute("SELECT * FROM miejsca_testy WHERE nazwa = %s", (nazwa_miejsca,))
                miejsce = cur.fetchone()

                if opakowanie is None and miejsce is None:
                    message = "Nie znaleziono takiego opakowania: " + nazwa_opakowania + " i takiego miejsca: " + nazwa_miejsca + ", dodaj je do bazy danych."
                elif opakowanie is None:
                    message = "Nie znaleziono takiego opakowania: " + nazwa_opakowania + ", dodaj je do bazy danych."
                elif miejsce is None:
                    message = "Nie znaleziono takiego miejsca: " + nazwa_miejsca + ", dodaj je do bazy danych."
                else:
                    # Sprawdzenie czy opakowanie już istnieje w przypisane_testy z innym barcode_miejsce
                    cur.execute(
                        "SELECT barcode_miejsce FROM przypisane_testy WHERE barcode_opak = %s",
                        (nazwa_opakowania,))
                    existing_barcode_miejsce = cur.fetchone()

                    if existing_barcode_miejsce and existing_barcode_miejsce[0] != nazwa_miejsca:
                        message = f"Opakowanie zbiorcze: {nazwa_opakowania} znajduje się już na miejscu: {existing_barcode_miejsce[0]}"
                    else:
                        cur.execute(
                            "INSERT INTO opakowania_miejsca (opakowanie_id, miejsce_id) VALUES (%s, %s)",
                            (opakowanie[0], miejsce[0]))
                        db.commit()
                        return redirect(
                                url_for('zostaw_opak_zbiorcze.zapisane_opak_zbiorcze', opakowanie=opakowanie[1], miejsce=nazwa_miejsca, message=message))
            elif nazwa_opakowania:  # Przypadek 2: Wprowadzono tylko nazwę opakowania
                cur.execute("SELECT * FROM opak_zbiorcze_testy WHERE nazwa = %s", (nazwa_opakowania,))
                opakowanie = cur.fetchone()

                if opakowanie is None:
                    message = "Nie znaleziono takiego opakowania: " + nazwa_opakowania + ", dodaj je do bazy danych."
                else:
                    cur.execute("SELECT barcode_miejsce FROM przypisane_testy WHERE barcode_opak = %s",
                                (nazwa_opakowania,))
                    przypisanie = cur.fetchone()

                    if przypisanie and przypisanie[0] != nazwa_opakowania:
                        barcode_miejsce = przypisanie[0]

                    else:
                        if przypisanie is not None: # Jeżeli opakowanie nie jest przypisane do żadnego miejsca
                            message = "Opakowanie: " + nazwa_opakowania + " jest już przypisane do innego miejsca"
            elif nazwa_miejsca:  # Przypadek 3: Wprowadzono tylko nazwę miejsca
                cur.execute("SELECT * FROM miejsca_testy WHERE nazwa = %s", (nazwa_miejsca,))
                miejsce = cur.fetchone()

                if miejsce is None: # Jeżeli miejsce nie istnieje w bazie danych
                    message = "Nie znaleziono takiego miejsca: " + nazwa_miejsca + ", dodaj je do bazy danych."

    return render_template('zostaw_opak_zbiorcze.html',opakowanie=opakowanie, message=message)

@zostaw_opak_zbiorcze_blueprint.route('/zapisane_opak_zbiorcze/<nazwa_opakowania>', methods=['GET'])
def zapisane_opak_zbiorcze(nazwa_opakowania, nazwa_miejsca):
    message = request.args.get('message')  # Pobranie komunikatu z parametrów URL
    db = baza_danych()
    cur = db.cursor()
    cur.execute("SELECT * FROM przypisane_testy ORDER BY id DESC LIMIT 1") # Wykonanie zapytania
    przypisane = cur.fetchall()
    db.close()
    return render_template('zapisane_opak_zbiorcze.html', opakowanie=nazwa_opakowania, miejsce=nazwa_miejsca, message=message, przypisane=przypisane)