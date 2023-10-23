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
from validate_email_address import validate_email
from configobj import ConfigObj
import hashlib


def log_reg():
    fenster = MpLogReg()
    fenster.setModal(True)

    fenster.exec_()


def hash_passwort(passwort):
    """Hasht das Passwort"""
    salt = b'q"\x0c\x00\'\xd8\xc4\xb8\xc4\xc5*\xa0X\x95\x8dp'

    passwort = passwort.encode('utf-8')
    iterationen = 10000

    # Sicherer Hashalgorithmus
    hash_algorithmus = "sha256"

    gehasht = hashlib.pbkdf2_hmac(hash_algorithmus, passwort, salt, iterationen)

    print(gehasht)
    return gehasht


def speichere_logindaten(benutzername: str, email: str, passwort: bytes):
    """Speichert die Logindaten in der Settings.ini Datei."""
    try:
        config = ConfigObj('settings.ini')
    except:
        # Neue Config Erstellen, wenn keien existiert
        config = ConfigObj()

    try:
        config['Login']['benutzername'] = benutzername
        config['Login']['email'] = email
        config['Login']['passwort'] = passwort
        config['Login']['eingeloggt'] = True

    except:
        # Fallst die Einträge noch nicht existieren: neue erstellen
        config['Login'] = {
            'benutzername': benutzername,
            'email': email,
            'passwort': passwort,
            'eingeloggt': True
        }

    config.write()


def lade_logindaten():
    try:
        config = ConfigObj('settings.ini')
    except:
        return None

    if not config['Login']['eingeloggt']:
        # Keine Logindaten gespeichert
        return None

    benutzername = config['Login']['benutzername']
    email = config['Login']['email']
    passwort = config['Login']['passwort']

    return benutzername, email, passwort


class MpLogReg(QDialog, Ui_mpLogReg):
    """
    In diesem Fenster kann sich der Benutzer anmelden bzw. ein Konto erstellen
    """
    def __init__(self, *args, **kwargs):
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
        self.txt_reg_email.editingFinished.connect(self.txt_reg_email_editingFinished)
        self.txt_log_email.editingFinished.connect(self.txt_log_email_editingFinished)

        self.net = Network()
        self.eingeloggt = False

    def txt_reg_email_editingFinished(self):
        """E-Mail nach Bearbeitung auf Gültigkeit überprüfen"""
        if validate_email(self.txt_reg_email.text()):
            self.lbl_reg_fehler_email.setText("")
        else:
            self.lbl_reg_fehler_email.setText("Ungültige E-Mail")

    def txt_log_email_editingFinished(self):
        """E-Mail nach Bearbeitung auf Gültigkeit überprüfen"""
        if validate_email(self.txt_log_email.text()):
            self.lbl_log_fehler_email.setText("")
        else:
            self.lbl_log_fehler_email.setText("Ungültige E-Mail")

    def cmd_zuLog_clicked(self):
        """Button um zum Login zu wechseln"""
        self.txt_log_email.setText(self.txt_reg_email.text())  # E-Mail übernehmen
        self.lbl_log_fehler_email.setText(self.lbl_reg_fehler_email.text())
        self.lbl_log_fehler.setText("")

        self.txt_log_email_editingFinished()

        self.stackedWidget.setCurrentIndex(0)

    def cmd_zuReg_clicked(self):
        """Button um zur Registrierung zu wechseln"""
        self.txt_reg_email.setText(self.txt_log_email.text())  # E-Mail übernehmen
        self.lbl_reg_fehler_email.setText(self.lbl_log_fehler_email.text())
        self.lbl_reg_fehler.setText("")

        self.stackedWidget.setCurrentIndex(1)

    def cmd_log_clicked(self):
        """Button Login wurde geklickt"""

        email = self.txt_log_email.text()
        passwort = hash_passwort(self.txt_log_passwort.text())

        ####

    def cmd_reg_clicked(self):
        """Button Registrieren wurde geklickt"""

        # Überprüfen, ob die E-Mail gültig ist
        if not validate_email(self.txt_reg_email.text()):
            self.lbl_reg_fehler.setText("Ungültige E-Mail!")
            print("Set ungültige EMail")
            return

        benutzername = self.txt_reg_benutzername.text()
        email = self.txt_reg_email.text()
        passwort = hash_passwort(self.txt_reg_passwort.text())

        erfolg = self.net.user_registrieren(benutzername, email, passwort)

        if erfolg == 1:
            self.lbl_reg_fehler.setText("Benutzername nicht mehr verfügbar!")
        elif erfolg == 2:
            self.lbl_reg_fehler.setText("Diese E-Mail Adresse ist bereits registriert!")

        speichere_logindaten(benutzername, email, passwort)

        self.eingeloggt = True
        self.close()


if __name__ == "__main__":
    import exception
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")

    window = MpLogReg()
    window.show()

    app.exec()
