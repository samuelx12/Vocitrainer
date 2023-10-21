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


class MpLogReg(QDialog, Ui_mpLogReg):
    """
    In diesem Fenster kann sich der Benutzer anmelden bzw. ein Konto erstellen
    """
    def __init__(self, hauptfenster, *args, obj=None, **kwargs):
        super(MpLogReg, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Login erforderlich")

    def logreg(self) -> bool:
        """

        :return: Ob die Anmeldung erfolgreich war
        """
