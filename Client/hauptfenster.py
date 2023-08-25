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
    def __init__(self, txt):
        """
        @param txt: Der Text den das Item zeigt
        """
        super().__init__()
        self.setText(0, txt)
        icon = QIcon()
        icon.addPixmap(QPixmap("res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap("res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.On)
        icon.addPixmap(QPixmap("res/icons/folder_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Selected, QIcon.Off)
        icon.addPixmap(QPixmap("res/icons/folder_open_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Selected, QIcon.On)
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

        # Explorer vorbereiten
        self.rootNode = self.trw_Explorer.invisibleRootItem()
        self.load_explorer()

    def cmd_beenden_clicked(self):
        self.close()

    def cmd_Setlernen_clicked(self):
        trainingsfenster = Trainingsfenster()
        trainingsfenster.setModal(True)

        trainingsfenster.exec_()

    def load_explorer(self):
        test = ExplorerItem("Ordner")
        self.rootNode.addChild(test)
