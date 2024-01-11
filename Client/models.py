# -*- coding: utf-8 -*-
"""
models.py
Hier werden alle Models (Modelle) gespeichert. In PyQt gibt es das Model-View Konzept. Im Fenster wird ein Widget
erstellt. Das Model, welches die Daten darin verwaltet wird allerdings einzel geschrieben und dann dem modelbased
Widget zugewiesen.
Der Vollständigkeit halber sei erwähnt, dass es auch sogenannte itembased Widgets gibt, die gleich wie ihre Verwandten
aussehen aber die in sich enthaltenen Daten anders verwalten.

Momentan ist hier nur das KartenModel.
"""
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QIcon
import typing
import sqlite3
from PyQt5.QtWidgets import QPushButton


class KartenModel(QAbstractTableModel):
    """
    Dies ist das QT-Model für die Tabelle in der die Karten im Hauptfenster angezeigt werden. Es verbindet die Datenbank
    mit der Gui.
    Aufbau der Daten: [karte_id, wort, fremdwort, definition, bemerkung, lernfortschritt, markiert, schwierigkeit]
    """
    def __init__(self, *args, dbconn, **kwargs):
        super(KartenModel, self).__init__(*args, **kwargs)
        # Referenz zur Datenbankverbindung abspeichern
        self.dbconn = dbconn
        self.geladenesSet = None
        self.daten = None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """Vorgegebene Funktion welche die Anzahl Zeilen zurückgeben muss."""
        # print("rowCount: ", len(self.daten))
        try:
            return len(self.daten)
        except:
            # Ausnahmefall beim Öffnen des Vocitrainers, wenn noch kein Set aktiv ist.
            return 0

    def columnCount(self, parent: QModelIndex = ...) -> int:
        """Vorgegebene Funktion welche die Anzahl Spalten zurückgeben muss."""
        return 6

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """
        Vorgegebene Funktion welche für einen Feld mit den Koordinaten (index.row() | index.column()) normalerweise
        den Inhalt (Wenn role = Qt.DisplayRole) erfragt.
        Aufbau der Daten: [karte_id, wort, fremdwort, definition, bemerkung, lernfortschritt, markiert, schwierigkeit]
        """

        reihe = index.row()
        spalte = index.column()

        spalte_kategorie_zuweisung = {
            0: 6,  # Stern zum Markieren
            1: 1,  # Wort
            2: 2,  # Fremdwort
            3: 3,  # Definition
            4: 4,  # Bemerkung
            5: 7,  # Schwierigkeit
            # 6: 5,  # Lernfortschritt
        }

        if role == Qt.UserRole:
            print("UserRole")

        kategorie = spalte_kategorie_zuweisung[spalte]

        if role in (Qt.DisplayRole, Qt.EditRole):
            # Text des Feldes
            if kategorie == 6:
                # Button für den Favoritenstern hinzufügen
                cmd_Markieren = QPushButton()
                cmd_Markieren.setText("Markieren")
                return cmd_Markieren
            elif kategorie in [1, 2, 3, 4]:
                # Diese Werte werden einfach eins zu eins zurückgegeben.
                return self.daten[reihe][kategorie]
            elif kategorie == 7:
                schwierigkeit = self.daten[reihe][7]
                if schwierigkeit == -1:
                    return "Unbekannt"
                elif schwierigkeit == 0:
                    return "Einfach"
                elif schwierigkeit == 1:
                    return "Mittelmässig"
                elif schwierigkeit == 2:
                    return "Schwer"
                elif schwierigkeit == 3:
                    return "Sehr schwer"
                else:
                    return "Unbekannt."

        elif role == Qt.ForegroundRole:
            # Farbe des Textes
            if kategorie == 7:
                # Farbe der Schwierigkeit zurückgeben
                schwierigkeit = self.daten[reihe][7]
                if schwierigkeit == -1:
                    return QColor(80, 80, 80)
                elif schwierigkeit == 0:
                    return QColor(0, 85, 0)
                elif schwierigkeit == 1:
                    return QColor(198, 132, 0)
                elif schwierigkeit == 2:
                    return QColor(170, 0, 0)
                elif schwierigkeit == 3:
                    return QColor(255, 0, 0)

        elif role == Qt.UserRole and spalte == 0:
            # Markieren Button zurückgeben
            cmd_Markieren = QPushButton()
            cmd_Markieren.setText("Hallo")

            return cmd_Markieren

        elif role == Qt.CheckStateRole and kategorie == 6:
            if self.daten[reihe][6] == 0:
                return Qt.Unchecked
            else:
                return Qt.Checked

        elif role == Qt.DecorationRole and spalte == 0:
            return QIcon(':/icons/res/icons/wifi_off_FILL0_wght400_GRAD0_opsz24.svg')

        # return self.daten[reihe][spalte]

    def lade_daten(self, set_id):
        """"
        Eigene Funktion, welche die Daten temporär aus der Datenbank lädt und in der Variable 'self.daten' speichert.
        Vorsicht: Muss immer (manuell) aufgerufen werden, wenn sich etwas an den Daten geändert hat.
        """
        self.beginResetModel()
        cursor = self.dbconn.cursor()

        # SQL-Abfrage, um bestimmte Spalten aus der Tabelle karte abzurufen
        query = """
        SELECT karte_id, wort, fremdwort, definition, bemerkung, lernfortschritt, markiert, schwierigkeit
        FROM karte WHERE set_id = ?
        """
        cursor.execute(query, (set_id,))
        result = cursor.fetchall()

        # Liste erstellen und Datensätze hinzufügen
        karte_liste = []
        for row in result:
            karte_liste.append([*row])

        self.daten = karte_liste
        self.geladenesSet = set_id  # Das aktuelle geladene Set anhand seiner ID abspeichern.

        self.endResetModel()

        # print(karte_liste)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        Vorgegebene Funktion, welche als Antwort die Eigenschaft des Feldes (Aktiv, Bearbeitbar...) zurück gibt.
        """
        if index.column() == 0:
            flags = \
                QtCore.Qt.ItemFlag.ItemIsEnabled | \
                QtCore.Qt.ItemFlag.ItemIsSelectable | \
                Qt.ItemFlag.ItemIsUserCheckable | \
                Qt.ItemFlag.ItemIsEditable
        else:
            flags =\
                QtCore.Qt.ItemFlag.ItemIsEditable |\
                QtCore.Qt.ItemFlag.ItemIsEnabled |\
                QtCore.Qt.ItemFlag.ItemIsSelectable

        return flags

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        """
        Vorgegebene Funktion welche es ermöglicht, den Inhalt der Tabelle direkt in dieser zu bearbeiten.
        Dazu wird zu erst die Karten Id in Erfahrung gebracht (In den Daten immer der erste Eintrag der zweiten Ebene).
        Mit dieser wird die Änderung gleich in die Datenbank geschrieben, und dann mit lade_daten auch in die
        self.daten Liste übernommen, von wo aus sie angezeigt wird.
        """
        reihe = index.row()
        spalte = index.column()

        if role in (Qt.DisplayRole, Qt.EditRole):
            print(f"Bearbeite: {index.row()}, {index.column()}")

            # Wenn die neue Version leer ist:
            if not value:
                return False

            # Zuerst muss die Karten ID herausgefunden werden,
            # damit die Änderung direkt in der Datenbank vorgenommen werden kann und
            # dann über die lade_daten Funktion auch in der Liste, der geladenen Karten gespeichert wird.
            karten_ID = self.daten[index.row][0]
            # print(karten_ID)

        elif role == Qt.CheckStateRole:
            if value == Qt.Checked:
                self.daten[reihe][6] = 1
            else:
                self.daten[reihe][6] = 0

        return True


if __name__ == '__main__':
    # Debug Skript, falls das File direkt ausgeführt wird.
    conn = sqlite3.connect('vocitrainerdb.db')
    tableview = KartenModel(dbconn=conn)
    tableview.lade_daten(1)
