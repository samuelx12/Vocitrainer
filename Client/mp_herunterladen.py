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


class mpHerunterladen(QDialog, Ui_mpHerunterladen):
    """
    Trainingsfenster
    """
    def __init__(self, *args, obj=None, **kwargs):
        super(mpHerunterladen, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Herunterladen")

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

    def cmd_schliessen_clicked(self):
        self.close()

    def txt_suche_textChanged(self):
        print("yes")
        resultate = self.net.vociset_suche(self.txt_suche.text(), 10)
        pass
