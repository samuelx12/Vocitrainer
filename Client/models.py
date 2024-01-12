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
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
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

        self.sprache = "Fremdsprache"

        self.spalte_kategorie_zuweisung = {
            0: 1,  # Wort
            1: 2,  # Fremdwort
            2: 3,  # Definition
            3: 4,  # Bemerkung
            4: 7,  # Schwierigkeit
            5: 5,  # Lernfortschritt
        }

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
        return len(self.spalte_kategorie_zuweisung)

    def headerData(self, section, orientation, role = ...):
        """Überschreibe die Funktion, um den Titel der Spalten zu bestimmen."""

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                kategorie = self.spalte_kategorie_zuweisung[section]
                if kategorie == 1:
                    return "Deutsch"
                elif kategorie == 2:
                    return self.sprache
                elif kategorie == 3:
                    return "Definition"
                elif kategorie == 4:
                    return "Bemerkung"
                elif kategorie == 5:
                    return "Lernfortschritt"
                elif kategorie == 6:
                    return "Markiert"
                elif kategorie == 7:
                    return "Schwierigkeit"
                else:
                    return QVariant()

            elif orientation == Qt.Vertical:
                return str(section + 1)

        # Sonst nichts zurückgeben (Nichts = QVariant())
        return QVariant()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """
        Vorgegebene Funktion welche für einen Feld mit den Koordinaten (index.row() | index.column()) normalerweise
        den Inhalt (Wenn role = Qt.DisplayRole) erfragt.
        Aufbau der Daten: [karte_id, wort, fremdwort, definition, bemerkung, lernfortschritt, markiert, schwierigkeit]
        """

        reihe = index.row()
        spalte = index.column()

        kategorie = self.spalte_kategorie_zuweisung[spalte]

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
            elif kategorie == 5:
                lernfortschritt = self.daten[reihe][5]
                if lernfortschritt == 0:
                    return "Ungelernt"
                elif lernfortschritt == 1:
                    return "Am lernen"
                elif lernfortschritt == 2:
                    return "Gelernt"
                else:
                    return "Lernfortschritt unbekannt"

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

        elif role == Qt.CheckStateRole and spalte == 0:
            if self.daten[reihe][6] == 0:
                return Qt.Unchecked
            else:
                return Qt.Checked

        elif role == Qt.DecorationRole and spalte == 0:
            if self.daten[reihe][6] == 0:
                return QIcon(':/icons/res/icons/rund_star_FILL0_wght400_GRAD0_opsz24.svg')
            else:
                return QIcon(':/icons/res/icons/rund_star_FILL1_wght400_GRAD0_opsz24.svg')

    def lade_daten(self, set_id):
        """"
        Eigene Funktion, welche die Daten temporär aus der Datenbank lädt und in der Variable 'self.daten' speichert.
        Vorsicht: Muss immer (manuell) aufgerufen werden, wenn sich etwas an den Daten geändert hat.
        """
        self.beginResetModel()
        cursor = self.dbconn.cursor()

        # Sprache herausfinden
        sql = """SELECT sprache FROM vociset WHERE set_id = ?"""
        cursor.execute(sql, (set_id,))
        self.sprache = cursor.fetchone()[0]

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

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        Vorgegebene Funktion, welche als Antwort die Eigenschaft des Feldes (Aktiv, Bearbeitbar...) zurück gibt.
        """
        kategorie = self.spalte_kategorie_zuweisung[index.column()]

        if kategorie == 7 or kategorie == 5:
            flags = \
                QtCore.Qt.ItemFlag.ItemIsEnabled | \
                QtCore.Qt.ItemFlag.ItemIsSelectable

        else:
            flags =\
                QtCore.Qt.ItemFlag.ItemIsEditable |\
                QtCore.Qt.ItemFlag.ItemIsEnabled |\
                QtCore.Qt.ItemFlag.ItemIsSelectable

        if index.column() == 0:
            flags |= Qt.ItemFlag.ItemIsUserCheckable

        return flags

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        """
        Vorgegebene Funktion welche es ermöglicht, den Inhalt der Tabelle direkt in dieser zu bearbeiten.
        Dazu wird zu erst die Karten Id in Erfahrung gebracht (In den Daten immer der erste Eintrag der zweiten Ebene).
        Mit dieser wird die Änderung gleich in die Datenbank geschrieben.
        """
        reihe = index.row()
        spalte = index.column()
        kategorie = self.spalte_kategorie_zuweisung[spalte]

        # Cursor für die Datenbank erstellen
        cursor = self.dbconn.cursor()

        # Id der Karte für Änderungen an der DB
        karten_ID = self.daten[index.row()][0]

        # ---------------- TEXT ÄNDERN ----------------
        if role == Qt.EditRole and kategorie in [1, 2, 3, 4]:

            # Wenn die neue Version leer ist (Bemerkung und Definition sind leer erlaubt)
            if not value and kategorie not in [1, 2]:
                cursor.close()
                return False

            # Änderung im Cache anpassen
            self.daten[reihe][kategorie] = value

            # Änderen in der DB speichern
            if kategorie == 1:
                sql = """UPDATE karte SET wort=? WHERE karte_id=?"""
            elif kategorie == 2:
                sql = """UPDATE karte SET fremdwort=? WHERE karte_id=?"""
            elif kategorie == 3:
                sql = """UPDATE karte SET definition=? WHERE karte_id=?"""
            else:
                sql = """UPDATE karte SET bemerkung=? WHERE karte_id=?"""

            cursor.execute(sql, (value, karten_ID))

            cursor.close()
            self.dbconn.commit()

        # ---------------- MARKIERUNG ÄNDERN ----------------
        elif role == Qt.CheckStateRole and spalte == 0:
            if value == Qt.Checked:
                markiert = 1
            else:
                markiert = 0

            # Cache updaten
            self.daten[reihe][6] = markiert

            # DB updaten
            sql = """UPDATE karte SET markiert=? WHERE karte_id=?"""
            cursor.execute(sql, (markiert, karten_ID))

            cursor.close()
            self.dbconn.commit()

        return True


if __name__ == '__main__':
    # Debug Skript, falls das File direkt ausgeführt wird.
    conn = sqlite3.connect('vocitrainerdb.db')
    tableview = KartenModel(dbconn=conn)
    tableview.lade_daten(1)
