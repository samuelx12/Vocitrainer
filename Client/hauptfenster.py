# -*- coding: utf-8 -*-
"""
hauptfenster.py
Diese Datei enthält eigentlich nur die Klasse Hauptfenster, welche von QMainWindow erbt. Das Hauptfenster ist das erste
Fenster, welches aufgeht. Das Programm läuft weiter, wenn Signale auftreten, welche mit einem Slot (Funktion) verbunden
wurden (Qt-Konzept)
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from models import KartenModel
from PyQt5.uic import loadUi
import sqlite3
from ui_hauptfenster import Ui_MainWindow
from trainingsfenster import Trainingsfenster


class ExplorerItem(QTreeWidgetItem):
    """
    Das Explorer Item ist eine Zeile in der Übersicht der Lernsets, die rechts angezeigt wird.
    """
    def __init__(self, txt, typ, id, parent: QTreeWidgetItem = None):
        """
        @param txt: Der Text den das Item zeigt
        """
        super().__init__(parent)
        self.setText(0, txt)
        icon = QIcon()
        self.id = id
        self.typ = typ
        if typ == "ordner":
            icon.addPixmap(QPixmap("res/icons/folder_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
            icon.addPixmap(QPixmap("res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.On)
        elif typ == "vociset":
            print("vociset Icon")
            icon.addPixmap(QPixmap("res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)

        self.setIcon(0, icon)

        # Das Item dem übergestellten Item zuordnen, falls dieses bekannt
        if parent:
            parent.addChild(self)

    def setActive(self, aktiv: bool) -> None:
        """Führt eine änderung des Icons durch je nach Status"""
        icon = QIcon()

        # Dicke Schrift an bzw. aus machen
        if self.typ == "vociset":
            font = QFont()
            font.setBold(aktiv)
            self.setFont(0, font)

        if aktiv:
            if self.typ == "vociset":
                icon.addPixmap(QPixmap("res/icons/note_stack_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Normal,
                               QIcon.Off)
            elif self.typ == "ordner":
                icon.addPixmap(QPixmap("res/icons/folder_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
                icon.addPixmap(QPixmap("res/icons/folder_open_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Normal,
                               QIcon.On)
        else:
            if self.typ == "vociset":
                icon.addPixmap(QPixmap("res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal,
                               QIcon.Off)
            elif self.typ == "ordner":
                icon.addPixmap(QPixmap("res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
                icon.addPixmap(QPixmap("res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.On)

        self.setIcon(0, icon)


class Hauptfenster(QMainWindow, Ui_MainWindow):
    """
    Diese Klasse repräsentiert das Hauptfenster. Sie erbt das Aussehen von der vom Qt-Designer exportierten Klasse.
    Dieses befindet sich in einer eigenen Datei, was den Workflow erheblich erleichtert, weil gleich die ganze
    Datei ohne Gefahr neu überschrieben werden kann.
    """
    def __init__(self, *args, obj=None, **kwargs):
        super(Hauptfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Vocitrainer")

        # Tabellen Model erstellen und zuweisen
        self.conn = sqlite3.connect('vocitrainerdb.db')
        print("Datenbankverbindung wurde erstellt")
        self.kartenModel = KartenModel(dbconn=self.conn)
        print("Model wurde erstellt")

        # Tabellen Model Daten laden
        self.kartenModel.lade_daten(1)

        # Model zuweisen
        self.tbv_Liste.setModel(self.kartenModel)
        print("Model wurde zugewiesen")

        # Signals und Slots verbinden
        self.cmd_Beenden.clicked.connect(self.cmd_beenden_clicked)
        self.cmd_SetLernen.clicked.connect(self.cmd_Setlernen_clicked)
        self.trw_Explorer.doubleClicked.connect(self.trw_Explorer_doubleClicked)

        # Explorer vorbereiten
        self.rootNode = self.trw_Explorer.invisibleRootItem()
        self.load_explorer()

        # Aktives Element im Explorer speichern
        self.aktiveItems = []

    def cmd_beenden_clicked(self):
        self.close()

    def cmd_Setlernen_clicked(self):
        trainingsfenster = Trainingsfenster()
        trainingsfenster.setModal(True)

        trainingsfenster.exec_()

    def load_explorer(self):
        def ebene_laden(parent, parent_id):
            # Ordner dieser Ebene laden
            query = "SELECT ordner_id, ordner_name, farbe, urordner_id FROM ordner WHERE urordner_id = ?"
            lade_cursor.execute(query, (parent_id,))
            result = lade_cursor.fetchall()

            # Resultat in Liste umwandeln
            ordner = []
            for reihe in result:
                ordner.append(reihe)

            # Vocisets dieser Ebene laden
            query = "SELECT set_id, set_name, beschreibung, sprache FROM vociset WHERE urordner_id = ?"
            lade_cursor.execute(query, (parent_id,))
            result = lade_cursor.fetchall()

            # Resultat in Liste umwandeln
            vocisets = []
            for reihe in result:
                vocisets.append(reihe)

            for i_ordner in ordner:
                neuer_ordner = ExplorerItem(i_ordner[1], "ordner", i_ordner[0], parent=parent)
                ebene_laden(neuer_ordner, i_ordner[0])

            for i_vociset in vocisets:
                neues_vociset = ExplorerItem(i_vociset[1], "vociset", i_vociset[0], parent=parent)

        lade_cursor = self.conn.cursor()
        test = ExplorerItem("Ordner", "ordner", 0)
        self.rootNode.addChild(test)
        explorer_index = []
        ebene_laden(self.rootNode, 1)

    def trw_Explorer_doubleClicked(self, item_index):
        """Funktion, die ausgeführt wird, wenn ein Item im Explorer doppelt geklickt wird."""
        # Das zugehörige Explorer Item bekommen
        item = self.trw_Explorer.itemFromIndex(item_index)

        if not isinstance(item, ExplorerItem):  # Eine Fehlerprüfung zur Sicherheit
            print("Nicht Explorer Item")
            return

        # Wenn ein Vociset doppeltgeklickt wurde, sollten die entsprechenden Daten geladen werden
        if item.typ == "vociset":
            self.kartenModel.lade_daten(item.id)

        # Alte Aktive entfernen
        for altesAktivesItem in self.aktiveItems:
            altesAktivesItem.setActive(False)

        # Aktiv Setzen vom Set und der Hirarchie darüber
        while item.parent():
            item.setActive(True)
            self.aktiveItems.append(item)
            item = item.parent()
        item.setActive(True)
        self.aktiveItems.append(item)
        item = item.parent()