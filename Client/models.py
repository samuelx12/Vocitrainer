# -*- coding: utf-8 -*-
"""
models.py
Hier werden alle Models (Modelle) gespeichert. In PyQt gibt es das Model-View Konzept. Im Fenster wird ein Widget
erstellt. Das Model, welches die Daten darin verwaltet wird allerdings einzel geschrieben und dann dem modelbased
Widget zugewiesen.
Der Vollständigkeit halber sei erwähnt, dass es auch sogenannte itembased Widgets gibt, die gleich wie ihre Verwandten
aussehen aber die in sich enthaltenen Daten anders verwalten.
"""
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
import typing
import sqlite3


class KartenModel(QAbstractTableModel):
    """
    Dies ist das QT-Model für die Tabelle in der die Karten im Hauptfenster angezeigt werden. Es verbindet die Datenbank
    mit der Gui.
    """
    def __init__(self, *args, dbconn, **kwargs):
        super(KartenModel, self).__init__(*args, **kwargs)
        # Referenz zur Datenbankverbindung abspeichern
        self.dbconn = dbconn
        self.geladenesSet = None
        self.daten = None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """Vorgegebene Funktion welche die Anzahl Zeilen zurückgeben muss."""
        print("rowCount: ", len(self.daten))
        return len(self.daten)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        """Vorgegebene Funktion welche die Anzahl Spalten zurückgeben muss."""
        print("columnCount: 5")
        return 5

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """
        Vorgegebene Funktion welche für einen Feld mit den Koordinaten (index.row() | index.column()) normalerweise
        den Inhalt (Wenn role = Qt.DisplayRole) erfragt.
        """
        if role == Qt.DisplayRole:
            reihe = index.row()
            spalte = index.column()
            print(f"Reihe: {reihe} Spalte: {spalte} Rückgabe: {self.daten[reihe][spalte]}")
            return self.daten[reihe][spalte]

    def lade_daten(self, set_id):
        """"
        Eigene Funktion, welche die Daten temporär aus der Datenbank lädt und in der Variable 'self.daten' speichert.
        Vorsicht: Muss immer (manuell) aufgerufen werden, wenn sich etwas an den Daten geändert hat.
        """
        cursor = self.dbconn.cursor()

        # SQL-Abfrage, um bestimmte Spalten aus der Tabelle karte abzurufen
        query = f"SELECT karte_id, wort, fremdwort, definition, markiert FROM karte WHERE set_id = ?"
        cursor.execute(query, (set_id,))
        result = cursor.fetchall()

        # Liste erstellen und Datensätze hinzufügen
        karte_liste = []
        for row in result:
            karte_liste.append(row)

        self.daten = karte_liste
        self.geladenesSet = set_id  # Das aktuelle geladene Set anhand seiner ID abspeichern.

        print(karte_liste)


if __name__ == '__main__':
    # Debug Skript, falls das File direkt ausgeführt wird.
    conn = sqlite3.connect('vocitrainerdb.db')
    tableview = KartenModel(dbconn=conn)
    tableview.lade_daten(1)
