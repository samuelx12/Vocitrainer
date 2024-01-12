# -*- coding: utf-8 -*-
"""
ueber.py
Dieses Fenster gibt kurze Info über den Vocitrainer und die Versionen von Qt und PyQt.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Client.res.ui_ueber import Ui_Ueber


class Ueber(QDialog, Ui_Ueber):
    """
    Dieses Fenster zeigt Infors über den Vocitrainer und Versionen von Qt/PyQt.
    """
    def __init__(self, versionen: dict, *args, **kwargs):
        super(Ueber, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfebutton ausblenden

        self.lbl_version_vocitrainer.setText("Vocitrainer: " + versionen["vocitrainer"])
        self.lbl_version_qt.setText("Qt: " + versionen["qt"])
        self.lbl_version_pyqt.setText("PyQt: " + versionen["pyqt"])

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/8), int(hoehe * 1/7))

        # Signale mit Slots verbinden
        self.cmd_Schliessen.clicked.connect(self.cmd_Schliessen_clicked)

    def cmd_Schliessen_clicked(self):
        self.close()
