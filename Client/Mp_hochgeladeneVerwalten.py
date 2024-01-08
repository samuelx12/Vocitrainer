# -*- coding: utf-8 -*-
"""
Mp_hochgeladeneVerwalten.py
Hier ist das Fenster, wo der Benutzer seine hochgeladenen Sets verwalten kann.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Client.res.ui_mp_hochgeladeneVerwalten import Ui_Mp_HochgeladeneVerwalten
from network import Network


class MpHochgeladeneVerwalten(QDialog, Ui_Mp_HochgeladeneVerwalten):
    """
    Hier kann der Benutzer die Sets verwalten, die er auf den Marketplace hochgeladen hat.
    Er kann sie löschen und umbenennen oder er kann nachsehen, wie häufig seine Sets heruntergeladen wurden.
    """
    def __init__(self, network: Network, *args, **kwargs):
        super(MpHochgeladeneVerwalten, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Herunterladen")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfebutton ausblenden
        self.net = network

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # Signale mit Slots verbinden
        self.cmd_schliessen.clicked.connect(self.cmd_schliessen_clicked)

        self.net = network
        inhalte = self.net.verwalten_info()
        self.lade_tabelle(inhalte)

    def cmd_schliessen_clicked(self) -> None:
        self.close()

    def lade_tabelle(self, inhalte):
        """
        Ladet die Tabelle mit "inhalte",
        wobei die Inhalte die Hochgeladenen Vocisets des angemeldeten Benutzers sind.
        inhalte = [set_id, set_name, beschreibung, sprache, anz_downloads]
        """
        print("Inhalte:", inhalte)
        self.inhalte = inhalte
        self.tbl_hochgeladeneSets.clear()
        self.tbl_hochgeladeneSets.setColumnCount(4)
        self.tbl_hochgeladeneSets.setRowCount(len(self.inhalte))

        self.tbl_hochgeladeneSets.setHorizontalHeaderLabels(["Name", "Sprache", "Downloads", "Löschen"])

        ueberschift = self.tbl_hochgeladeneSets.horizontalHeader()
        ueberschift.setSectionResizeMode(QHeaderView.Stretch)

        for reihe in range(len(self.inhalte)):
            # Erste Spalte: Set Name
            self.tbl_hochgeladeneSets.setItem(reihe, 0, QTableWidgetItem(self.inhalte[reihe][1]))

            # Zweite Spalte: Sprache
            self.tbl_hochgeladeneSets.setItem(reihe, 1, QTableWidgetItem(self.inhalte[reihe][3]))

            # Dritte Spalte: Anzahl Downloads
            self.tbl_hochgeladeneSets.setItem(reihe, 2, QTableWidgetItem(str(self.inhalte[reihe][4])))

            # Vierte Spalte: 'Löschen'-Button
            loeschen_button = QPushButton("Löschen")
            loeschen_button.setIcon(QIcon("res/icons/delete_FILL0_wght500_GRAD0_opsz40.svg"))
            loeschen_button.clicked.connect(self.set_loeschen_button_clicked)
            self.tbl_hochgeladeneSets.setCellWidget(reihe, 3, loeschen_button)

    def set_loeschen_button_clicked(self):
        """
        Diese Methode wird ausgeführt, wenn einer der Löschen-Buttons gelickt wurde.
        Nachdem die ID des dazugehörigen Sets herausgefunden wurde, wird der Lösch-Befehl an den Server gesendet.
        """

        clicked_button = self.sender()
        if clicked_button:
            button_index = self.tbl_hochgeladeneSets.indexAt(clicked_button.pos())
            if button_index.isValid():
                reihe = button_index.row()
                set_id = self.inhalte[reihe][0]
                self.net.verwalten_aktion(set_id, 0)

                # Erfolgsnachricht auf dem Button ausgeben
                erfolg_button = QPushButton("Gelöscht")
                erfolg_button.setIcon(QIcon("res/icons/delete_FILL0_wght500_GRAD0_opsz40.svg"))
                self.tbl_hochgeladeneSets.setCellWidget(reihe, 3, erfolg_button)
