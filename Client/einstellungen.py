# -*- coding: utf-8 -*-
"""
einstellungen.py
Hier kann der Benutzer verschiedene Sachen einstellen.
"""
import os
import shutil

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from res.ui_einstellungen import Ui_Einstellungen
from configobj import ConfigObj
from Mp_LogReg import log_reg, msg_verbindungsFehler


class Einstellungen(QDialog, Ui_Einstellungen):
    """
    Einstellungen
    """
    def __init__(self, q_app: QApplication, *args, **kwargs):
        super(Einstellungen, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfebutton ausblenden
        self.angemeldet = False
        self.frame_willkommenEinstellungen.setVisible(False)

        self.q_app = q_app

        # Einstellungen laden
        self.einstellungen_laden()

        # Signale mit Slots verbinden
        self.cmd_ok.clicked.connect(self.cmd_ok_clicked)
        self.cmd_abbrechen.clicked.connect(self.cmd_abbrechen_clicked)
        self.cmd_uebernehmen.clicked.connect(self.cmd_uebernehmen_clicked)
        self.cmd_DatenbankExportieren.clicked.connect(self.cmd_DatenbankExportieren_clicked)
        self.cmd_anzeigen.clicked.connect(self.cmd_anzeigen_clicked)
        self.cmd_xxMelden.clicked.connect(self.cmd_xxMelden_clicked)
        self.cmd_kontoLoeschen.clicked.connect(self.cmd_kontoLoeschen_clicked)

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
            self.box_fokusmodus.setChecked(bool(int(config['Lernen']['fokusmodus'])))

            # Sektion Login
            self.angemeldet = bool(int(config['Login']['eingeloggt']))
            if self.angemeldet:
                self.lbl_profilStatus.setText("Angemeldet")
                self.cmd_xxMelden.setText("Abmelden")
                self.cmd_kontoLoeschen.setVisible(True)
            else:
                self.lbl_profilStatus.setText("Abgemeldet")
                self.cmd_xxMelden.setText("Anmelden")
                self.cmd_kontoLoeschen.setVisible(False)

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
            self.box_fokusmodus.setChecked(False)

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

        # Stil setzen
        if self.cmb_stil.currentText() == "Vocitrainer":
            self.q_app.setStyle("fusion")
        elif self.cmb_stil.currentText() == "Windows":
            self.q_app.setStyle("WindowsVista")
        elif self.cmb_stil.currentText() == "Nostalgisch":
            self.q_app.setStyle("Windows")

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
            'definitionLernen': int(self.box_definitionLernen.isChecked()),
            'fokusmodus': int(self.box_fokusmodus.isChecked())
        }

        # Sektion Login
        config['Login'] = {
            'benutzername': self.benutzername,
            'email': self.email,
            'passwort': self.passwort,
            'eingeloggt': int(self.angemeldet)
        }

        config.write()

    def msg_verbindungsFehler(self):
        """
        Zeigt eine MessageBox an, dass die Verbindung fehlgeschlagen sei.
        :return: None
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QIcon(':/icons/res/icons/wifi_off_FILL0_wght400_GRAD0_opsz24.svg'))
        msg.setWindowTitle("Verbindung fehlgeschlagen")
        msg.setText(
            "Fehler bei der Verbindung mit dem Server!\n"
            + "Überprüfen sie ihre Internetverbindung."
        )
        msg.exec_()

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
            self.cmd_kontoLoeschen.setVisible(False)
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
                self.cmd_kontoLoeschen.setVisible(True)

                self.lbl_email.setVisible(self.angemeldet)
                self.email = config['Login']['email']
                self.lbl_email.setText(f"E-Mail: {self.email}")

                self.lbl_benutzername.setVisible(self.angemeldet)
                self.benutzername = config['Login']['benutzername']
                self.lbl_benutzername.setText(f"Benutzername: {self.benutzername}")

                self.lbl_passwort.setVisible(self.angemeldet)
                self.passwort = config['Login']['passwort']
                self.lbl_passwort.setText("Passwort: *********")
            elif erfolg is False:
                self.msg_verbindungsFehler()

    def cmd_kontoLoeschen_clicked(self):
        """'Konto löschen'-Button geklickt."""

        # Warnung anzeigen, dass das Löschen entgültig ist
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon(':/icons/res/icons/delete_forever_FILL0_wght400_GRAD0_opsz24.svg'))
        msg.setWindowTitle("Endgültige Löschung des Kontos")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setText(
            "Achtung! Die Löschung des Kontos ist endgültig!\nAlle von Ihnen hochgeladenen Sets werden gelöscht!\n\n"
            "Wollen Sie Ihr Konto wirklich löschen?"
        )
        antwort = msg.exec_()

        if antwort == QMessageBox.No:
            # Abbruch
            return

        erfolg, net = log_reg()

        if not erfolg:
            msg_verbindungsFehler()
            return

        erfolg = net.konto_loeschen()

        if not erfolg:
            # Fehlermeldung anzeigen
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon(':/icons/res/icons/error_FILL0_wght400_GRAD0_opsz24.svg'))
            msg.setWindowTitle("Unerwarteter beim Löschen")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText(
                "Es ist ein unerwarteter Fehler beim Löschen des Kontos aufgetreten."
            )
            antwort = msg.exec_()
        else:
            # Erfolgsmeldung anzeigen
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon(':/icons/res/icons/info_FILL0_wght400_GRAD0_opsz24.svg'))
            msg.setWindowTitle("Konto gelöscht")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText(
                "Ihr Konto wurde gelöscht und die Einstellungen gespeichert."
            )
            antwort = msg.exec_()

            # Abmelden
            self.email = ""
            self.benutzername = ""
            self.passwort = ""
            self.angemeldet = False
            self.cmd_xxMelden.setText("Anmelden")
            self.lbl_profilStatus.setText("Abgemeldet")
            self.cmd_kontoLoeschen.setVisible(False)
            self.lbl_email.setVisible(False)
            self.lbl_benutzername.setVisible(False)
            self.lbl_passwort.setVisible(False)

            self.einstellungen_speichern()

    def cmd_DatenbankExportieren_clicked(self):
        """
        Der Benutzer möchte die vocitrainer.db exportieren.
        """

        # Gewünschter Speicherort in Erfahrung bringen.
        file_dialog = QFileDialog(parent=self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)  # Einstellen auf Speichermodus

        # Setzen Sie den vorgeschlagenen Dateinamen und den Filter für die Dateierweiterung
        file_dialog.setDefaultSuffix('vocidb')
        file_dialog.setNameFilter("Datenbank (*.db);;Alle Dateien (*.*)")

        # Anpassen des Dialogtitels
        file_dialog.setWindowTitle("Exportieren")
        file_dialog.setLabelText(QFileDialog.Accept, "Exportieren")

        # Dialog anzeigen und das Ergebnis überprüfen
        result = file_dialog.exec_()
        if result == QFileDialog.Accepted:
            ziel = file_dialog.selectedFiles()[0]
            print("Zielpfade:", ziel)
        else:
            return

        ursprung = os.path.join(os.getcwd(), "vocitrainerdb.db")

        try:
            shutil.copy(ursprung, ziel)

            # Erfolgsmeldung
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon(':/icons/res/icons/info_FILL0_wght400_GRAD0_opsz24.svg'))
            msg.setWindowTitle("Erfolg")
            msg.setText(
                "Die Datenbank wurde erfolgreich exportiert!"
            )
            msg.exec_()
        except FileNotFoundError:
            # Fehlermeldung
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(QIcon(':/icons/res/icons/error_FILL0_wght400_GRAD0_opsz24.svg'))
            msg.setWindowTitle("Fehler")
            msg.setText(
                "Die Datenbank wurde nicht gefunden und konnte deshalb nicht exportiert werden\n" +
                "Möglicherweise ist ihre Installation beschädigt!"
            )
            msg.exec_()
        except PermissionError:
            # Fehlermeldung
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(QIcon(':/icons/res/icons/error_FILL0_wght400_GRAD0_opsz24.svg'))
            msg.setWindowTitle("Zugriff verweigert")
            msg.setText(
                "Der Zugriff auf den Zielordner wurde verweigert. "
                "Stellen sie sicher, dass sie die nötigen Berechtigungen haben."
            )
            msg.exec_()
        except Exception as e:
            # Fehlermeldung
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(QIcon(':/icons/res/icons/error_FILL0_wght400_GRAD0_opsz24.svg'))
            msg.setWindowTitle("Unerwarteter Fehler")
            msg.setText(
                "Ein unerwarteter Fehler ist aufgetreten:\n" + str(e)
            )
            msg.exec_()
