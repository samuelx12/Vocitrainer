# -*- coding: utf-8 -*-
"""
ueber.py
Dieses Fenster gibt kurze Info über den Vocitrainer und die Versionen von Qt und PyQt.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from res.ui_ueber import Ui_Ueber
import webbrowser


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
        self.cmd_ZurWebseite.clicked.connect(self.cmd_ZurWebseite_clicked)
        self.cmd_Lizenz.clicked.connect(self.cmd_Lizenz_clicked)

    def cmd_Lizenz_clicked(self):
        # Lizenzinformationen anzeigen
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon(':/icons/res/icons/license_FILL0_wght400_GRAD0_opsz40.svg'))
        msg.setWindowTitle("Lizenz")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Close)
        msg.setDefaultButton(QMessageBox.Close)
        msg.button(QMessageBox.Yes).setText("Lizenz öffnen")
        msg.button(QMessageBox.Close).setText("Schliessen")
        msg.setText(
            "Vocitrainer - einfach und effizient Vokabeln lernen\n"
            "Copyright © 2024  Samuel Barmet\n\n"

            "This program is free software: you can redistribute it and/or modify "
            "it under the terms of the GNU General Public License as published by "
            "the Free Software Foundation, either version 3 of the License, or "
            "(at your option) any later version. "
            "This program is distributed in the hope that it will be useful,"
            " but WITHOUT ANY WARRANTY; without even the implied warranty of"
            " MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n"
            """See the GNU General Public License for more details."""
        )
        antwort = msg.exec_()

        if antwort == QMessageBox.Yes:
            webbrowser.open("https://www.gnu.org/licenses/gpl-3.0.de.html")

    def cmd_ZurWebseite_clicked(self):
        webbrowser.open("https://vocitrainer.admuel.ch")

    def cmd_Schliessen_clicked(self):
        self.close()
