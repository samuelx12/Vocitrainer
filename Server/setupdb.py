# -*- coding: utf-8 -*-
"""
setupdb.py
Dieses Skript erstellt eine Testdatenbank mit Testdaten für den Server
"""

import sqlite3
from datetime import datetime

# Verbindung zur Datenbank herstellen (erstellt die Datenbank, wenn sie nicht existiert)
conn = sqlite3.connect('serverdb.db')
cursor = conn.cursor()

# Tabelle 'user' erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        passwort TEXT,
        benutzername TEXT UNIQUE,
        gesperrt INTEGER,
        erstellung DATETIME
    )
''')

# Tabelle 'vociset' erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vociset (
        set_id INTEGER PRIMARY KEY,
        set_name TEXT,
        beschreibung TEXT,
        sprache TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user (user_id)
    )
''')

# Tabelle 'karte' erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS karte (
        karte_id INTEGER PRIMARY KEY,
        wort TEXT,
        fremdwort TEXT,
        definition TEXT,
        bemerkung TEXT,
        set_id INTEGER,
        FOREIGN KEY (set_id) REFERENCES vociset (set_id)
    )
''')

# Testdaten in die Tabelle 'set' einfügen
cursor.execute(
    f"INSERT INTO user (email, passwort, benutzername, gesperrt, erstellung) "
    f"VALUES ('test@barmet.ch', 'pass', 'testname', 0, ?)",
    [datetime.now()]
)
cursor.execute(
    f"INSERT INTO user (email, passwort, benutzername, gesperrt, erstellung) "
    f"VALUES ('muster@barmet.ch', 'pass', 'mustername', 0, ?)",
    [datetime.now()]
)

# Testdaten in die Tabelle 'set' einfügen
cursor.execute(
    "INSERT INTO vociset (set_name, beschreibung, sprache) VALUES ('servSet 1', 'servBeschreibung Set 1', 'Englisch')")
cursor.execute(
    "INSERT INTO vociset (set_name, beschreibung, sprache) VALUES "
    "('servSet 2', 'servBeschreibung Set 2 Farben', 'Englisch')"
)

# Testdaten in die Tabelle 'karte' einfügen
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id) 
VALUES ('servHaus', 'servHouse', 'servEine Unterkunft für Menschen.', 'Bsp: Ich wohne in einem Haus.', 1)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id) 
VALUES ('servAuto', 'servCar', 'servEin Fahrzeug mit vier Rädern.', 'Bsp: Er fährt mit dem Auto.', 1)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id) 
VALUES ('servApfel', 'servApple', 'servEine runde Frucht zum Essen.', 'Bsp: Du isst einen Apfel', 1)""")

cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id) 
VALUES ('servBlau', 'servblue', 'servDie Frabe des Himmels.', 'Der Himmel ist blau.', 2)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id) 
VALUES ('servGrün', 'servgreen', 'Dservie Farbe der Pflanzen.', 'Das Gras ist grün.', 2)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id) 
VALUES ('servRot', 'servred', 'servDie Farbe der Liebe.', 'Ich zeichne eine rote Blume.', 2)""")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()
