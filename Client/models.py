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
        self.dbconn = dbconn
        self.geladenesSet = None
        self.daten = None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        print(len(self.daten))
        return len(self.daten)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        print(len(max(self.daten, key=len)))
        return len(max(self.daten, key=len))

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            reihe = index.row()
            spalte = index.column()
            print(self.daten[reihe][spalte])
            return self.daten[reihe][spalte]

    def lade_daten(self, set_id):
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
        self.geladenesSet = set_id

        print(karte_liste)

if __name__ == '__main__':
    conn = sqlite3.connect('vocitrainerdb.db')
    tableview = KartenModel(dbconn=conn)
    tableview.lade_daten(1)
