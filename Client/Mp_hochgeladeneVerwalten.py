# -*- coding: utf-8 -*-
"""
Mp_hochgeladeneVerwalten.py
Hier ist das Fenster, wo der Benutzer seine hochgeladenen Sets verwalten kann.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Client.res.qt.ui_mp_hochgeladeneVerwalten import Ui_Mp_HochgeladeneVerwalten
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

    def cmd_schliessen_clicked(self) -> None:
        self.close()

    def lade_tabell(self, inhalte):
        """
        Ladet die Tabelle mit "inhalte",
        wobei die Inhalte die Hochgeladenen Vocisets des angemeldeten Benutzers sind.
        """
        self.inhalte = inhalte
        self.tbl_hochgeladeneSets.clear()

