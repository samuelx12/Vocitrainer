# -*- coding: utf-8 -*-
"""
Mp_Hochladen.py
Hier ist das Fenster in welchem der Benutzer noch Name und Tags anpasst bevor es hochgeladen wird.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Client.res.ui_ueber import Ui_Ueber


class Ueber(QDialog, Ui_Ueber):
    """
    Hier kann der Benutzer noch Name, Sprache und Tags anpassen, bevor das Set hochgeladen wird.
    """
    def __init__(self, version: str, *args, **kwargs):
        super(Ueber, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfebutton ausblenden

        self.lbl_version.setText("Version " + version)

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/8), int(hoehe * 1/7))

        # Signale mit Slots verbinden
        self.cmd_Schliessen.clicked.connect(self.cmd_Schliessen_clicked)

    def cmd_Schliessen_clicked(self):
        self.close()
