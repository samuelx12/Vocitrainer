# -*- coding: utf-8 -*-
"""
mp_herunterladen.py
Hier ist das Herunterladen Fenster des Menu Marketplace.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_mp_herunterladen import Ui_mpHerunterladen
from network import Network
import sqlite3


class MpHerunterladen(QDialog, Ui_mpHerunterladen):
    """
    Trainingsfenster
    """
    def __init__(self, hauptfenster, *args, obj=None, **kwargs):
        super(MpHerunterladen, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Herunterladen")
        self.hauptfenster = hauptfenster

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # Signale mit Slots verbinden
        self.cmd_schliessen.clicked.connect(self.cmd_schliessen_clicked)
        self.txt_suche.textChanged.connect(self.txt_suche_textChanged)

        # self.setStyleSheet(
        #     """font: 14pt "MS Shell Dlg 2";"""
        # )

        # Serververbindung erstellen
        self.net = Network()

        self.DBCONN = sqlite3.connect('vocitrainerdb.db')
        self.CURSOR = self.DBCONN.cursor()

    def cmd_schliessen_clicked(self) -> None:
        self.close()

    def txt_suche_textChanged(self):
        print("yes")
        if self.txt_suche.text().split():
            resultate = self.net.vociset_suche(self.txt_suche.text(), 10)
            print(resultate)

            # Tabelle neu laden
            self.lade_tabelle(resultate)

    def lade_tabelle(self, resultate):
        """Ladet die Tabelle mit den Suchresultaten neu"""

        self.such_resultate = resultate

        self.tbl_suche.clear()
        self.tbl_suche.setColumnCount(2)
        self.tbl_suche.setRowCount(len(self.such_resultate))

        for reihe in range(len(self.such_resultate)):
            # In die erste Spalte kommt der Set Name:
            self.tbl_suche.setItem(reihe, 0, QTableWidgetItem(self.such_resultate[reihe][1]))

            # Erstellen eines Buttons für die zweite Spalte
            herunterladen_button = QPushButton("Herunterladen")
            herunterladen_button.clicked.connect(self.set_herunterladen_button_clicked)

            self.tbl_suche.setCellWidget(reihe, 1, herunterladen_button)

    def set_herunterladen_button_clicked(self):
        """
        Diese Methode wird aktiv, wenn einer der Herunterladenbuttons in der Tabelle geklickt wurde.
        Sie findet die ID des Heruntergeladenen Buttons heraus und gibt den Download in Auftrag.
        """
        clicked_button = self.sender()
        if clicked_button:
            button_index = self.tbl_suche.indexAt(clicked_button.pos())
            if button_index.isValid():
                reihe = button_index.row()
                set_id = self.such_resultate[reihe][0]
                self.set_herunterladen(set_id)

    def set_herunterladen(self, set_id: int) -> None:
        """
        Lädt die Datensätze eines Sets und der zugehörigen Karten herunter.
        :param set_id: Die ID des zu herunterladenden Sets
        :return: None
        """
        print(f"Lade Set mit der ID {set_id} herunter.")
        vociset_datensatz, karten_datensaetze = self.net.vociset_herunterladen(set_id)
        print(vociset_datensatz)
        print(karten_datensaetze)

        # SQL-Query um das Vociset in der Datenbank zu speichern
        query = """
        INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES (?, ?, ?, 1)
        """
        self.CURSOR.execute(query, [vociset_datensatz[i] for i in range(1, 4)])
        gespeicherte_set_id = self.CURSOR.lastrowid

        # Schleife um die Karten einzufügen
        query = f"""
        INSERT INTO karte (wort, fremdwort, definition, lernfortschritt, markiert, set_id)
        VALUES (?, ?, ?, 0, 0, {gespeicherte_set_id})
        """
        for i in range(len(karten_datensaetze)):
            self.CURSOR.execute(query, [karten_datensaetze[i][j] for j in range(1, 4)])

        self.DBCONN.commit()

        self.hauptfenster.load_explorer()
