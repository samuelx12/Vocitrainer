# -*- coding: utf-8 -*-
"""
Mp_LogReg.py
Dieses Fenster wird immer angezeigt, wenn der Benutzer nicht angemeldet ist und
ein Konto für seine nächste Aktion braucht.
Man erstellt dann ein LogReg-Fenster und führt dessen Methode LogReg aus.

"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_mp_logreg import Ui_mpLogReg
from network import Network


class MpLogReg(QDialog, Ui_mpLogReg):
    """
    In diesem Fenster kann sich der Benutzer anmelden bzw. ein Konto erstellen
    """
    def __init__(self, *args, obj=None, **kwargs):
        super(MpLogReg, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Login erforderlich")
        self.lbl_log_fehler.setText("")
        self.lbl_reg_fehler.setText("")
        self.stackedWidget.setCurrentIndex(0)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfe Button ausblenden

        # Signale und Slots verbinden
        self.cmd_zuLog.clicked.connect(self.cmd_zuLog_clicked)
        self.cmd_zuReg.clicked.connect(self.cmd_zuReg_clicked)
        self.cmd_log.clicked.connect(self.cmd_log_clicked)
        self.cmd_reg.clicked.connect(self.cmd_reg_clicked)

    def logreg(self) -> bool:
        """

        :return: Ob die Anmeldung erfolgreich war
        """
        try:
            self.net = Network()
        except:
            # Todo Fehlermeldung
            return False

        return True

    def cmd_zuLog_clicked(self):
        """Button um zum Login zu wechseln"""
        self.txt_log_email.setText(self.txt_reg_email.text())  # E-Mail übernehmen
        self.lbl_log_fehler.setText("")
        self.stackedWidget.setCurrentIndex(0)

    def cmd_zuReg_clicked(self):
        """Button um zur Registrierung zu wechseln"""
        self.txt_reg_email.setText(self.txt_log_email.text())  # E-Mail übernehmen
        self.lbl_reg_fehler.setText("")
        self.stackedWidget.setCurrentIndex(1)

    def cmd_log_clicked(self):
        """Button Login wurde geklickt"""
        pass

    def cmd_reg_clicked(self):
        """Button Registrieren wurde geklickt"""


if __name__ == "__main__":
    import exception
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")

    window = MpLogReg()
    window.show()

    app.exec()
