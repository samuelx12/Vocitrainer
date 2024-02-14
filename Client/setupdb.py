# -*- coding: utf-8 -*-
"""
setupdb.py
Ein Skript, das eine frische, saubere Datenbank erstellt und mit Testdaten befüllt.
Fallst die Datenbank bereits besteht, werden einfach noch mehr Testdaten eingefüllt.
"""

import sqlite3
from contextlib import suppress


def updateDB(dbconn: sqlite3.Connection, testdaten_hinzufuegen: bool = False):
    """
    Fügt Tabellen hinzu falls welche fehlen.
    :param dbconn: Die Verbindung zur Datenbank
    :param testdaten_hinzufuegen: True falls Testdaten eingefügt werden sollen.
    :return: None
    """

    # Cursor erstellen
    cursor = dbconn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # Tabelle 'ordner' erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordner (
            ordner_id INTEGER PRIMARY KEY,
            ordner_name TEXT,
            farbe TEXT,
            urordner_id INTEGER,
            FOREIGN KEY (urordner_id) REFERENCES ordner (ordner_id) ON DELETE CASCADE
        )
    ''')

    # Tabelle 'set' erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vociset (
            set_id INTEGER PRIMARY KEY,
            set_name TEXT,
            beschreibung TEXT,
            sprache TEXT,
            urordner_id INTEGER,
            FOREIGN KEY (urordner_id) REFERENCES ordner (ordner_id) ON DELETE CASCADE
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
            lernfortschritt INTEGER,
            markiert INTEGER,
            schwierigkeit INTEGER,
            set_id INTEGER,
            FOREIGN KEY (set_id) REFERENCES vociset (set_id) ON DELETE CASCADE
        )
    ''')

    # Tabelle 'karte' erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loesung (
            loesung_id INTEGER PRIMARY KEY,
            korrekt INTEGER,
            fremdwort TEXT,
            karte_id INTEGER,
            FOREIGN KEY (karte_id) REFERENCES karte (karte_id) ON DELETE CASCADE
        )
    ''')

    # Testdaten in die Tabelle 'ordner' einfügen
    with suppress(Exception):
        cursor.execute("INSERT INTO ordner (ordner_name, farbe, urordner_id) VALUES ('ROOT', 'Normal', NULL)")

    if not testdaten_hinzufuegen:
        # Änderungen speichern und Verbindung schließen
        dbconn.commit()
        return

    cursor.execute("INSERT INTO ordner (ordner_name, farbe, urordner_id) VALUES ('Unterordner', 'Grün', 1)")
    cursor.execute("INSERT INTO ordner (ordner_name, farbe, urordner_id) VALUES ('U2 Ordner', 'Grün', 2)")

    # Testdaten in die Tabelle 'set' einfügen
    cursor.execute(
        "INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) "
        "VALUES ('Set 1', 'Beschreibung Set 1', 'Englisch', 1)"
    )
    cursor.execute(
        "INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES "
        "('Set 2', 'Beschreibung Set 2 Farben', 'Englisch', 2)"
    )

    # Testdaten in die Tabelle 'karte' einfügen
    cursor.execute("""
    INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id, lernfortschritt, markiert, schwierigkeit) 
    VALUES ('Haus', 'House', 'Eine Unterkunft für Menschen.', 'Bsp: Ich wohne in einem Haus.', 1, 0, 1, -1)""")
    cursor.execute("""
    INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id, lernfortschritt, markiert, schwierigkeit) 
    VALUES ('Auto', 'Car', 'Ein Fahrzeug mit vier Rädern.', 'Bsp: Er fährt mit dem Auto.', 1, 0, 0, -1)""")
    cursor.execute("""
    INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id, lernfortschritt, markiert, schwierigkeit) 
    VALUES ('Apfel', 'Apple', 'Eine runde Frucht zum Essen.', 'Bsp: Du isst einen Apfel', 1, 0, 1, -1)""")

    cursor.execute("""
    INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id, lernfortschritt, markiert, schwierigkeit) 
    VALUES ('blau', 'blue', 'Die Frabe des Himmels.', 'Der Himmel ist blau.', 2, 0, 1, -1)""")
    cursor.execute("""
    INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id, lernfortschritt, markiert, schwierigkeit) 
    VALUES ('grün', 'green', 'Die Farbe der Pflanzen.', 'Das Gras ist grün.', 2, 0, 0, -1)""")
    cursor.execute("""
    INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id, lernfortschritt, markiert, schwierigkeit) 
    VALUES ('rot', 'red', 'Die Farbe der Liebe.', 'Ich zeichne eine rote Blume.', 2, 0, 1, -1)""")
    cursor.execute("""
    INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id, lernfortschritt, markiert, schwierigkeit) 
    VALUES ('gelb', 'yellow', 'Die Farbe der Fröhlichkeit.', 'Die Sonne ist Gelb.', 2, 0, 1, -1)""")

    # Änderungen speichern und Verbindung schließen
    dbconn.commit()
