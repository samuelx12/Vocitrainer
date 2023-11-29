# -*- coding: utf-8 -*-
"""
Mp_Hochladen.py
Hier ist das Fenster in welchem der Benutzer noch Name und Tags anpasst bevor es hochgeladen wird.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_mp_hochladen import Ui_Mp_Hochladen
from network import Network
import sqlite3


class MpHochladen(QDialog, Ui_Mp_Hochladen):
    """
    Hier kann der Benutzer noch Name, Sprache und Tags anpassen, bevor das Set hochgeladen wird.
    """
    def __init__(self, network: Network, set_id: int, *args, **kwargs):
        super(MpHochladen, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Set hochladen")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfebutton ausblenden
        self.net = network
        self.set_id = set_id

        # Eigene DB Verbindung erstellen
        self.dbconn = sqlite3.connect('vocitrainerdb.db')
        self.CURSOR = self.dbconn.cursor()

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # Signale mit Slots verbinden
        self.cmd_abbrechen.clicked.connect(self.cmd_abbrechen_clicked)
        self.cmd_hochladen.clicked.connect(self.cmd_hochladen_clicked)

    def cmd_abbrechen_clicked(self):
        self.close()

    def cmd_hochladen_clicked(self):
        self.hochladen(self.set_id)
        self.close()

    def hochladen(self, set_id: int):
        """
        Hier wird das Vociset wirklich hochgeladen
        :param set_id: set_id in der vocitrainerdb.db des hochzuladenen Vocisets
        :return:
        """

        # Daten des Vocisets aus der UI laden
        set_name = self.txt_name.text()
        beschreibung = self.txt_tags.toPlainText()
        sprache = self.cmb_sprache.currentText()

        # SQL-Query der die Karten Datensätze lädt
        query = """SELECT wort, fremdwort, definition, bemerkung, set_id FROM karte WHERE set_id = ?"""
        self.CURSOR.execute(query, (set_id,))
        karten_datensaetze = self.CURSOR.fetchall()

        self.net.vociset_hochladen(
            (set_name, beschreibung, sprache),
            karten_datensaetze
        )
