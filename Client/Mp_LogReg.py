# -*- coding: utf-8 -*-
"""
Mp_LogReg.py

LogReg Fenster
    Dieses Fenster wird immer angezeigt, wenn der Benutzer nicht angemeldet ist und
    ein Konto für seine nächste Aktion braucht.
log_reg Funktion
    Das wichtigste hierdrin ist dabei aber die Funktion log_reg(). Sie vereinfacht das ganze, indem sie selbst
    nachschaut, ob das LogReg Fenster geöffnet werden muss oder ob der Benutzer bereits angemeldet ist.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from res.ui_mp_logreg import Ui_mpLogReg
from network import Network
from validate_email import validate_email
from configobj import ConfigObj
import hashlib
import typing


def log_reg() -> typing.Tuple[typing.Union[bool, None], typing.Union[Network, None]]:
    """
    Versucht den Benutzer einzuloggen. Wenn möglich geschieht es mit seinen bereits gespeicherten Nutzerdaten
    in den Einstellungen, ansonsten wird ein Login/Registrierung (LogReg) Fenster aufgemacht
    :return: Ein Tuple aus
        bool Erfolg, None wenn Abbruch
        Eingeloggten Network bzw. None bei Misserfolg
    """
    logindaten = lade_logindaten()
    if logindaten:
        # print("Logindaten vorhanden")
        # Fall 1: Benutzer hat sich bereits einmal eingeloggt -> automatisch verbinden
        try:
            net = Network()
        except Exception as e:
            # raise e  #  Entfernen
            return False, None

        email = logindaten[1]
        passwort = logindaten[2]
        erfolg = net.user_einloggen(email, passwort)

        if erfolg:
            return True, net

    # Fall 2: Keine Logindaten gespeichert -> LogReg-Fenster für Anmeldung öffnen
    # oder automatische Anmeldung (Fall 1) fehlgeschlagen
    try:
        fenster = MpLogReg()
    except:
        return False, None

    fenster.setModal(True)

    fenster.exec_()

    if fenster.eingeloggt:
        return True, fenster.net
    else:
        return None, None


def hash_passwort(passwort):
    """Hasht das Passwort"""
    salt = b'q"\x0c\x00\'\xd8\xc4\xb8\xc4\xc5*\xa0X\x95\x8dp'

    passwort = passwort.encode('utf-8')
    iterationen = 10000

    # Sicherer Hashalgorithmus
    hash_algorithmus = "sha256"

    gehasht = hashlib.pbkdf2_hmac(hash_algorithmus, passwort, salt, iterationen)

    return gehasht


def speichere_logindaten(benutzername: str, email: str, passwort: bytes):
    """Speichert die Logindaten in der Settings.ini Datei."""
    try:
        config = ConfigObj('settings.ini')
    except:
        # Neue Config Erstellen, wenn keine existiert
        config = ConfigObj()

    try:
        config['Login']['benutzername'] = benutzername
        config['Login']['email'] = email
        config['Login']['passwort'] = passwort
        config['Login']['eingeloggt'] = 1

    except:
        # Fallst die Einträge noch nicht existieren: neue erstellen
        config['Login'] = {
            'benutzername': benutzername,
            'email': email,
            'passwort': passwort,
            'eingeloggt': 1
        }

    config.write()


def lade_logindaten():
    """
    Versucht die Logindaten aus den Einstellungen zu laden.
    :return: None bei Misserfolg / benutername, email, passwort bei Erfolg
    """
    try:
        config = ConfigObj('settings.ini')
    except:
        return None

    if not bool(int(config['Login']['eingeloggt'])):
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
        self.setWindowTitle("Anmelden")
        self.lbl_log_fehler.setText("")
        self.lbl_reg_fehler.setText("")
        self.stackedWidget.setCurrentIndex(0)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfe Button ausblenden

        # Signale und Slots verbinden
        self.cmd_zuLog.clicked.connect(self.cmd_zuLog_clicked)
        self.cmd_zuReg.clicked.connect(self.cmd_zuReg_clicked)
        self.cmd_log.clicked.connect(self.cmd_log_clicked)
        self.cmd_reg.clicked.connect(self.cmd_reg_clicked)
        self.cmd_reg2.clicked.connect(self.cmd_reg2_clicked)
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
        self.setWindowTitle("Anmelden")

        self.txt_log_email_editingFinished()

        self.stackedWidget.setCurrentIndex(0)

    def cmd_zuReg_clicked(self):
        """Button um zur Registrierung zu wechseln"""
        self.txt_reg_email.setText(self.txt_log_email.text())  # E-Mail übernehmen
        self.lbl_reg_fehler_email.setText(self.lbl_log_fehler_email.text())
        self.lbl_reg_fehler.setText("")
        self.setWindowTitle("Registrieren")

        self.stackedWidget.setCurrentIndex(1)

    def cmd_log_clicked(self):
        """Button Login wurde geklickt"""

        email = self.txt_log_email.text()
        passwort = hash_passwort(self.txt_log_passwort.text())

        erfolg = self.net.user_einloggen(email, passwort)

        if erfolg:
            self.eingeloggt = True
            # Hier müsste eigentlich noch vom Server der zugehörige Benutzername geladen werden
            speichere_logindaten("Unbekannt", email, passwort)
            self.close()
            return
        else:
            self.lbl_log_fehler.setText("Login fehlgeschlagen: E-Mail oder Passwort inkorrekt!")
            return

    def cmd_reg_clicked(self):
        """Button Registrieren wurde geklickt"""

        # Überprüfen, ob die E-Mail gültig ist
        if not validate_email(self.txt_reg_email.text()):
            self.lbl_reg_fehler.setText("Ungültige E-Mail!")

            return

        self.benutzername = self.txt_reg_benutzername.text()
        self.email = self.txt_reg_email.text()
        self.passwort = hash_passwort(self.txt_reg_passwort.text())

        erfolg = self.net.user_registrieren(self.benutzername, self.email, self.passwort)

        if erfolg == 1:
            self.lbl_reg_fehler.setText("Benutzername nicht mehr verfügbar!")
        elif erfolg == 2:
            self.lbl_reg_fehler.setText("Diese E-Mail Adresse ist bereits registriert!")
        elif erfolg == 3:
            self.lbl_reg_fehler.setText("Fehler beim Versenden des Bestätigungcodes. Versuchen sie es später nochmals!")
        else:
            # Registierung erfolgreich angefordert, jetzt muss nur noch der Bestätigungscode gesendet werden.
            self.stackedWidget.setCurrentIndex(2)

    def cmd_reg2_clicked(self):
        """
        Button 'Registierung abschliessen' wurde geklickt.
        """
        try:
            code = int(self.txt_reg2_Code.text())
        except:
            self.lbl_reg2_Fehler.setText("Ungültiger Code!")
            return

        erfolg = self.net.registierung_abschliessen(code)

        if not erfolg:
            self.lbl_reg2_Fehler.setText("Falscher Code!")
            return
        else:
            # Registierung korrekt abgeschlossen
            speichere_logindaten(self.benutzername, self.email, self.passwort)

            self.eingeloggt = True
            self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")

    window = MpLogReg()
    window.show()

    app.exec()
