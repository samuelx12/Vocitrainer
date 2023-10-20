# -*- coding: utf-8 -*-
"""
Mp_herunterladen.py
Hier ist das Herunterladen Fenster des Menu Marketplace.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_importCSV import Ui_ImportCSV
from network import Network
import sqlite3


class ImportCSV(QDialog, Ui_ImportCSV):
    """
    In diesem Fenster befinden sich die Einstellungen, damit danach ein Vociset aus einer Datei importiert werden kann.
    """
    def __init__(self, hauptfenster, *args, obj=None, **kwargs):
        super(ImportCSV, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.hauptfenster = hauptfenster

        self.int_spalteWort.setValue(1)
        self.int_spalteFremdwort.setValue(2)

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # Signale mit Slots verbinden
        self.cmd_abbrechen.clicked.connect(self.cmd_abbrechen_clicked)
        self.cmd_durchsuchen.clicked.connect(self.cmd_durchsuchen_clicked)
        self.txt_pfad.textChanged.connect(self.txt_pfad_textChanged)

        self.DBCONN = sqlite3.connect('vocitrainerdb.db')
        self.CURSOR = self.DBCONN.cursor()

        # Einige Widgets ausblenden
        self.lbl_Warnung.setVisible(False)
        self.lbl_FehlerPfad.setVisible(False)
        self.txt_Vorschau.setVisible(False)
        self.lbl_Vorschau.setVisible(False)

    def txt_pfad_textChanged(self):
        """Der Pfad wurde geändert -> Vorschau aktualisieren"""
        try:
            with open(self.txt_pfad.text(), 'r') as file:
                zeilen = file.readlines()[:3]
                inhalt = ''.join(zeilen)
                self.txt_Vorschau.setPlainText(inhalt)
                self.txt_Vorschau.setVisible(True)
                self.lbl_Vorschau.setVisible(True)
                self.lbl_FehlerPfad.setVisible(False)
        except Exception:
            self.lbl_FehlerPfad.setText(
                "Fehler beim Öffnen der Vorschau. "
                "Stellen sie sicher, dass der Pfad korrekt und die Datei unbeschädigt ist."
            )
            self.txt_Vorschau.setVisible(False)
            self.lbl_Vorschau.setVisible(False)
            self.lbl_FehlerPfad.setVisible(True)

    def cmd_abbrechen_clicked(self) -> None:
        """Abbrechen wurde geklickt -> Fenster schliessen"""
        self.close()

    def cmd_durchsuchen_clicked(self) -> None:
        """
        Der Durchsuchen Button öffnet ein Fenster, wo eine CSV oder TXT Datei ausgewählt werden kann,
        deren Pfad danach in das entsprechende Feld geschrieben wird.
        """
        optionen = QFileDialog.Options()
        datei_browser = QFileDialog(self, options=optionen)
        datei_browser.setFileMode(QFileDialog.ExistingFile)

        # Filter setzen, um nur CSV- und TXT-Dateien anzuzeigen
        datei_browser.setNameFilter("CSV- und TXT-Dateien (*.csv *.txt)")

        if datei_browser.exec_():
            ausgewaehlte_dateien = datei_browser.selectedFiles()
            if ausgewaehlte_dateien:
                file_path = ausgewaehlte_dateien[0]
                self.txt_pfad.setText(file_path)

