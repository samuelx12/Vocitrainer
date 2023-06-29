import sqlite3

# Verbindung zur Datenbank herstellen (erstellt die Datenbank, wenn sie nicht existiert)
conn = sqlite3.connect('vocitrainerdb.db')
cursor = conn.cursor()

# Tabelle 'ordner' erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ordner (
        ordner_id INTEGER PRIMARY KEY,
        ordner_name TEXT,
        farbe TEXT,
        urordner_id INTEGER,
        FOREIGN KEY (urordner_id) REFERENCES ordner (ordner_id)
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

# Testdaten in die Tabelle 'ordner' einfügen
cursor.execute("INSERT INTO ordner (ordner_name, farbe, urordner_id) VALUES ('Hauptordner', 'Blau', NULL)")
cursor.execute("INSERT INTO ordner (ordner_name, farbe, urordner_id) VALUES ('Unterordner', 'Grün', 1)")

# Testdaten in die Tabelle 'set' einfügen
cursor.execute(
"INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES ('Set 1', 'Beschreibung Set 1', 'Deutsch', 1)")
cursor.execute(
"INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES ('Set 2', 'Beschreibung Set 2', 'Englisch', 2)")

# Testdaten in die Tabelle 'karte' einfügen
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, set_id, lernfortschritt, markiert) 
VALUES ('Haus', 'House', 'Eine Unterkunft für Menschen.', 1, 50, 1)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, set_id, lernfortschritt, markiert) 
VALUES ('Auto', 'Car', 'Ein Fahrzeug mit vier Rädern.', 1, 75, 0)""")
cursor.execute("""INSERT INTO karte (wort, fremdwort, definition, set_id, lernfortschritt, markiert) 
VALUES ('Apfel', 'Apple', 'Eine runde Frucht zum Essen.', 2, 25, 1)""")


# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel


def create_connection():
    # Verbindung zur SQLite-Datenbank herstellen
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('vocitrainerdb.db')

    if not db.open():
        print('Fehler beim Öffnen der Datenbank')
        return False

    return True


def create_table_view():
    # Modell für das QTableView erstellen
    model = QSqlQueryModel()
    query = QSqlQuery()

    # SQL-Abfrage, um alle Daten aus der Tabelle 'karte' abzurufen
    query.exec_("SELECT * FROM karte")
    model.setQuery(query)

    # QTableView erstellen und das Modell zuweisen
    table_view = QTableView()
    table_view.setModel(model)

    return table_view


if __name__ == '__main__':
    app = QApplication(sys.argv)

    if not create_connection():
        sys.exit(1)

    table_view = create_table_view()

    # Hauptfenster erstellen und den QTableView hinzufügen
    main_window = QMainWindow()
    main_window.setCentralWidget(table_view)
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec_())