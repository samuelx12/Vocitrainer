# -*- coding: utf-8 -*-
"""
Mp_herunterladen.py
Hier ist das Herunterladen Fenster des Menu Marketplace.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Client.res.qt.ui_mp_herunterladen import Ui_mpHerunterladen
from network import Network
import sqlite3


class MpHerunterladen(QDialog, Ui_mpHerunterladen):
    """
    Hier kann der Benutzer Sets von anderen Benutzern vom Marketplace suchen und herunterladen.
    """
    def __init__(self, hauptfenster, *args, obj=None, **kwargs):
        super(MpHerunterladen, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Herunterladen")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfebutton ausblenden
        self.hauptfenster = hauptfenster

        # "Starten sie mit der Suche ..."-Meldung anzeigen
        self.stackedWidget.setCurrentIndex(1)
        self.lbl_emoji.setVisible(False)
        self.lbl_Meldung.setText("Starten sie mit der Suche...")
        self.lbl_Meldung.setStyleSheet("""color: rgb(0, 85, 0); font: italic 10pt "Segoe UI";""")
        self.txt_suche.setFocus()

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # Signale mit Slots verbinden
        self.cmd_schliessen.clicked.connect(self.cmd_schliessen_clicked)
        self.txt_suche.textChanged.connect(self.txt_suche_textChanged)
        self.cmd_refresh.clicked.connect(self.txt_suche_textChanged)

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
        if self.txt_suche.text().split():
            resultate = self.net.vociset_suche(self.txt_suche.text(), 10)
            print(resultate)
            if resultate:
                # Tabelle neu laden
                self.lade_tabelle(resultate)
                self.stackedWidget.setCurrentIndex(0)
            else:
                # Keine Treffer
                self.stackedWidget.setCurrentIndex(1)
                self.lbl_Meldung.setText("Keine Treffer!")
                self.lbl_emoji.setVisible(True)
                self.lbl_Meldung.setStyleSheet("""color: rgb(170, 0, 0); font: italic 10pt "Segoe UI";""")

        else:
            self.tbl_suche.clear()
            self.tbl_suche.setColumnCount(0)
            self.tbl_suche.setRowCount(0)

            self.stackedWidget.setCurrentIndex(1)
            self.lbl_Meldung.setText("Starten sie mit der Suche...")
            self.lbl_emoji.setVisible(False)
            self.lbl_Meldung.setStyleSheet("""color: rgb(0, 85, 0); font: italic 10pt "Segoe UI";""")

    def lade_tabelle(self, resultate):
        """Ladet die Tabelle mit den Suchresultaten neu"""

        self.such_resultate = resultate

        self.tbl_suche.clear()
        self.tbl_suche.setColumnCount(2)
        self.tbl_suche.setRowCount(len(self.such_resultate))

        # Spaltenbreite festlegen
        header = self.tbl_suche.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)

        # Die erste Spalte nimmt 2/3 des Platzes ein
        header.resizeSection(0, int(self.width() * 2 / 3.3))

        # Die zweite Spalte nimmt 1/3 des Platzes ein
        header.resizeSection(1, int(self.width() * 1 / 3.3))

        for reihe in range(len(self.such_resultate)):
            # In die erste Spalte kommt der Set Name:
            self.tbl_suche.setItem(reihe, 0, QTableWidgetItem(self.such_resultate[reihe][1]))

            # Erstellen eines Buttons für die zweite Spalte
            herunterladen_button = QPushButton("Herunterladen")
            herunterladen_button.setIcon(QIcon("res/icons/download_FILL0_wght500_GRAD0_opsz40.svg"))
            herunterladen_button.clicked.connect(self.set_herunterladen_button_clicked)

            self.tbl_suche.setCellWidget(reihe, 1, herunterladen_button)

    def set_herunterladen_button_clicked(self):
        """
        Diese Methode wird aktiv, wenn einer der Herunterladenbuttons in der Tabelle geklickt wurde.
        Sie findet die ID des geklickten Buttons heraus und gibt den Download in Auftrag.
        """
        clicked_button = self.sender()
        if clicked_button:
            button_index = self.tbl_suche.indexAt(clicked_button.pos())
            if button_index.isValid():
                reihe = button_index.row()
                set_id = self.such_resultate[reihe][0]
                self.set_herunterladen(set_id, reihe)

    def set_herunterladen(self, set_id: int, zeile: int) -> None:
        """
        Lädt die Datensätze eines Sets und der zugehörigen Karten herunter.
        :param zeile: Die Reihe in der Tabelle, um später dort eine Erfolgsmeldung zu zeigen
        :param set_id: Die ID des zu herunterladenden Sets
        :return: None
        """
        # print(f"Lade Set mit der ID {set_id} herunter.")
        vociset_datensatz, karten_datensaetze = self.net.vociset_herunterladen(set_id)
        # print(vociset_datensatz)
        # print(karten_datensaetze)

        # SQL-Query um das Vociset in der Datenbank zu speichern
        query = """
        INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES (?, ?, ?, 1)
        """
        self.CURSOR.execute(query, [vociset_datensatz[i] for i in range(1, 4)])
        gespeicherte_set_id = self.CURSOR.lastrowid

        # Schleife um die Karten einzufügen
        query = f"""
        INSERT INTO karte (wort, fremdwort, definition, bemerkung, lernfortschritt, markiert, schwierigkeit, set_id)
        VALUES (?, ?, ?, ?, 0, 0, 0, {gespeicherte_set_id})
        """
        for i in range(len(karten_datensaetze)):
            self.CURSOR.execute(query, [karten_datensaetze[i][j] for j in range(1, 5)])

        self.DBCONN.commit()
        self.hauptfenster.load_explorer()

        # erfolgsmeldungsitem = QTableWidgetItem("Heruntergeladen")
        # erfolgsmeldungsitem.setIcon("res/icons/download_FILL0_wght500_GRAD0_opsz40.svg")
        # self.tbl_suche.setItem(reihe, 1, erfolgsmeldungsitem)

        herunterladen_button = QPushButton("Heruntergeladen")
        herunterladen_button.setIcon(QIcon("res/icons/download_done_FILL0_wght500_GRAD0_opsz40.svg"))
        self.tbl_suche.setCellWidget(zeile, 1, herunterladen_button)

        # print("Erfolgsmeldung!")
        # print(zeile)
