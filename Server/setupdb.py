# -*- coding: utf-8 -*-
"""
setupdb.py
Dieses Skript erstellt eine Testdatenbank mit Testdaten für den Server
"""

import sqlite3

# Verbindung zur Datenbank herstellen (erstellt die Datenbank, wenn sie nicht existiert)
conn = sqlite3.connect('serverdb.db')
cursor = conn.cursor()

# Tabelle 'set' erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vociset (
        set_id INTEGER PRIMARY KEY,
        set_name TEXT,
        beschreibung TEXT,
        sprache TEXT,
        urordner_id INTEGER,
        FOREIGN KEY (urordner_id) REFERENCES ordner (ordner_id)
    )
''')


# Tabelle 'karte' erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS karte (
        karte_id INTEGER PRIMARY KEY,
        wort TEXT,
        fremdwort TEXT,
        definition TEXT,
        lernfortschritt INTEGER,
        markiert INTEGER,
        set_id INTEGER,
        FOREIGN KEY (set_id) REFERENCES vociset (set_id)
    )
''')

# Testdaten in die Tabelle 'set' einfügen
cursor.execute(
"INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES ('servSet 1', 'servBeschreibung Set 1', 'Englisch', 1)")
cursor.execute(
"INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES ('servSet 2', 'servBeschreibung Set 2 Farben', 'Englisch', 2)")

# Testdaten in die Tabelle 'karte' einfügen
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, set_id, lernfortschritt, markiert) 
VALUES ('servHaus', 'servHouse', 'servEine Unterkunft für Menschen.', 1, 50, 1)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, set_id, lernfortschritt, markiert) 
VALUES ('servAuto', 'servCar', 'servEin Fahrzeug mit vier Rädern.', 1, 75, 0)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, set_id, lernfortschritt, markiert) 
VALUES ('servApfel', 'servApple', 'servEine runde Frucht zum Essen.', 1, 25, 1)""")

cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, set_id, lernfortschritt, markiert) 
VALUES ('servBlau', 'servblue', 'servDie Frabe des Himmels.', 2, 50, 1)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, set_id, lernfortschritt, markiert) 
VALUES ('servGrün', 'servgreen', 'Dservie Farbe der Pflanzen.', 2, 75, 0)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, set_id, lernfortschritt, markiert) 
VALUES ('servRot', 'servred', 'servDie Farbe der Liebe.', 2, 25, 1)""")


# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()
