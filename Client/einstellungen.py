# -*- coding: utf-8 -*-
"""
einstellungen.py
Hier kann der Benutzer verschiedene Sachen einstellen.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from res.ui_einstellungen import Ui_Einstellungen
from configobj import ConfigObj
from Mp_LogReg import log_reg


class Einstellungen(QDialog, Ui_Einstellungen):
    """
    Einstellungen
    """
    def __init__(self, *args, **kwargs):
        super(Einstellungen, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfebutton ausblenden
        self.angemeldet = False
        self.frame_willkommenEinstellungen.setVisible(False)

        # Einstellungen laden
        self.einstellungen_laden()

        # Signale mit Slots verbinden
        self.cmd_ok.clicked.connect(self.cmd_ok_clicked)
        self.cmd_abbrechen.clicked.connect(self.cmd_abbrechen_clicked)
        self.cmd_uebernehmen.clicked.connect(self.cmd_uebernehmen_clicked)
        self.cmd_anzeigen.clicked.connect(self.cmd_anzeigen_clicked)
        self.cmd_xxMelden.clicked.connect(self.cmd_xxMelden_clicked)

    def einstellungen_laden(self):
        """
        Diese Funktion ladet die Einstellungen aus der settings.ini Datei in die UI.
        :return bool Erfolg
        """

        try:
            # Versuche Einstellungen zu laden
            config = ConfigObj("settings.ini")

            # Sektion Allgemein
            self.cmb_stil.setCurrentText(config['Allgemein']['stil'])
            self.box_willkommenMeldung.setChecked(bool(int(config['Allgemein']['willkommenMeldung'])))
            self.cmb_sprache.setCurrentText(config['Allgemein']['neuesSetSprache'])

            # Sektion Lernen
            if int(config['Lernen']['mz']) == 7:
                self.cmb_mz.setCurrentText("7 - Normal")
            else:
                self.cmb_mz.setCurrentText(str(int(config['Lernen']['mz'])))

            ft = int(config['Lernen']['ft'])
            if ft == 1:
                self.cmb_ft.setCurrentText("Tief")
            elif ft == 2:
                self.cmb_ft.setCurrentText("Normal")
            else:
                self.cmb_ft.setCurrentText("Hoch")

            self.box_definitionLernen.setChecked(bool(int(config['Lernen']['definitionLernen'])))

            # Sektion Login
            self.angemeldet = bool(int(config['Login']['eingeloggt']))
            if self.angemeldet:
                self.lbl_profilStatus.setText("Angemeldet")
                self.cmd_xxMelden.setText("Abmelden")
            else:
                self.lbl_profilStatus.setText("Abgemeldet")
                self.cmd_xxMelden.setText("Anmelden")

            self.lbl_email.setVisible(self.angemeldet)
            self.email = config['Login']['email']
            self.lbl_email.setText(f"E-Mail: {self.email}")

            self.lbl_benutzername.setVisible(self.angemeldet)
            self.benutzername = config['Login']['benutzername']
            self.lbl_benutzername.setText(f"Benutzername: {self.benutzername}")

            self.lbl_passwort.setVisible(self.angemeldet)
            self.passwort = config['Login']['passwort']
            self.lbl_passwort.setText("Passwort: *********")

        except Exception as e:
            # raise e
            # Bei Fehler einfach Standart Einstellungen laden, welche dann neu gespeichert werden können.
            config = ConfigObj("settings.ini")

            # Sektion Allgemein
            self.cmb_stil.setCurrentText("Vocitrainer")
            self.box_willkommenMeldung.setChecked(True)
            self.cmb_sprache.setCurrentText("Englisch")

            # Sektion Lernen
            self.cmb_mz.setCurrentText("7-Normal")
            self.cmb_ft.setCurrentText("Normal")
            self.box_definitionLernen.setChecked(False)

            # Sektion Login
            self.angemeldet = False
            self.lbl_profilStatus.setText("Abgemeldet")
            self.cmd_xxMelden.setText("Anmelden")

            self.email = ""
            self.benutzername = ""
            self.passwort = ""

    def einstellungen_speichern(self):
        """
        Diese Funktion speicher die Einstellungen in der settings.ini,
        welche in der UI geladen und durch den Benutzer angepasst worden sind.
        """

        # Neues ConfigObj erstellen, da sowieso alle Einstellungen neu gespeichert werden.
        config = ConfigObj('settings.ini')

        # Sektion Allgemein
        config['Allgemein'] = {
            'stil': self.cmb_stil.currentText(),
            'willkommenMeldung': int(self.box_willkommenMeldung.isChecked()),
            'neuesSetSprache': self.cmb_sprache.currentText()
        }

        # Sektion Lernen
        mz_ui = self.cmb_mz.currentText()
        if mz_ui == "7 - Normal":
            mz = 7
        else:
            mz = int(mz_ui)

        ft_ui = self.cmb_ft.currentText()
        if ft_ui == "Tief":
            ft = 1
        elif ft_ui == "Normal":
            ft = 2
        else:
            ft = 3

        config['Lernen'] = {
            'mz': mz,
            'ft': ft,
            'definitionLernen': int(self.box_definitionLernen.isChecked())
        }

        # Sektion Login
        config['Login'] = {
            'benutzername': self.benutzername,
            'email': self.email,
            'passwort': self.passwort,
            'eingeloggt': int(self.angemeldet)
        }

        config.write()

    def cmd_ok_clicked(self):
        """'OK'-Button wurde geklickt."""
        self.einstellungen_speichern()
        self.close()

    def cmd_abbrechen_clicked(self):
        """'OK'-Button wurde geklickt."""
        self.close()

    def cmd_uebernehmen_clicked(self):
        """'OK'-Button wurde geklickt."""
        self.einstellungen_speichern()

    def cmd_anzeigen_clicked(self):
        """'OK'-Button wurde geklickt."""
        pass

    def cmd_xxMelden_clicked(self):
        """'OK'-Button wurde geklickt."""
        if self.angemeldet:
            # Abmelden
            self.email = ""
            self.benutzername = ""
            self.passwort = ""
            self.angemeldet = False
            self.cmd_xxMelden.setText("Anmelden")
            self.lbl_profilStatus.setText("Abgemeldet")
            self.lbl_email.setVisible(False)
            self.lbl_benutzername.setVisible(False)
            self.lbl_passwort.setVisible(False)
        else:
            # Anmelden
            erfolg, net = log_reg()
            if erfolg:
                # LogReg Fenster speichert die Anmeldedaten in den Einstellungen
                # Deshalb werden diese jetzt von dort neu geladen
                config = ConfigObj("settings.ini")

                # Sektion Login
                self.angemeldet = bool(int(config['Login']['eingeloggt']))
                self.lbl_profilStatus.setText("Angemeldet")
                self.cmd_xxMelden.setText("Abmelden")

                self.lbl_email.setVisible(self.angemeldet)
                self.email = config['Login']['email']
                self.lbl_email.setText(f"E-Mail: {self.email}")

                self.lbl_benutzername.setVisible(self.angemeldet)
                self.benutzername = config['Login']['benutzername']
                self.lbl_benutzername.setText(f"Benutzername: {self.benutzername}")

                self.lbl_passwort.setVisible(self.angemeldet)
                self.passwort = config['Login']['passwort']
                self.lbl_passwort.setText("Passwort: *********")
