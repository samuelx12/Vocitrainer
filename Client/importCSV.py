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
    Trainingsfenster
    """
    def __init__(self, hauptfenster, *args, obj=None, **kwargs):
        super(ImportCSV, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.hauptfenster = hauptfenster

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # Signale mit Slots verbinden
        self.cmd_abbrechen.clicked.connect(self.cmd_abbrechen_clicked)
        self.cmd_durchsuchen.clicked.connect(self.cmd_durchsuchen_clicked)

        self.DBCONN = sqlite3.connect('vocitrainerdb.db')
        self.CURSOR = self.DBCONN.cursor()

    def cmd_abbrechen_clicked(self) -> None:
        self.close()

    def cmd_durchsuchen_clicked(self) -> None:
        optionen = QFileDialog.Options()
        datei_browser = QFileDialog(self, options=optionen)
        datei_browser.setFileMode(QFileDialog.ExistingFile)

        # Filter setzen, um nur CSV- und TXT-Dateien anzuzeigen
        datei_browser.setNameFilter("Textdateien (*.txt);;CSV-Dateien (*.csv)")

        if datei_browser.exec_():
            ausgewaehlte_dateien = datei_browser.selectedFiles()
            if ausgewaehlte_dateien:
                file_path = ausgewaehlte_dateien[0]
                self.txt_pfad.setText(file_path)

