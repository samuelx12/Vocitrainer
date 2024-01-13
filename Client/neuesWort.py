# -*- coding: utf-8 -*-
"""
neuesWort.py
Hier ist das Fenster in welchem der Benutzer noch Name und Tags anpasst bevor es hochgeladen wird.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from res.ui_neuesWort import Ui_NeuesWort
from sqlite3 import Connection


class NeuesWort(QDialog, Ui_NeuesWort):
    """
    Der Benutzer kann mit dieser Gui seinen Sets neue Wörter hinzufügen.
    """
    def __init__(self, set_id: int, dbconn: Connection, *args, **kwargs):
        super(NeuesWort, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfebutton ausblenden
        self.lbl_erfolg.setVisible(False)

        self.set_id = set_id
        self.dbconn = dbconn

        self.wort_zaehler = 0

        # Sprache herausfinden
        cursor = self.dbconn.cursor()
        sql = """SELECT sprache FROM main.vociset WHERE set_id = ?"""
        cursor.execute(sql, (set_id,))
        self.sprache = cursor.fetchone()[0]
        cursor.close()

        self.lbl_fremdsprache.setText(f"{self.sprache}: ")

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/8), int(hoehe * 1/7))

        # Signale mit Slots verbinden
        self.cmd_hinzufuegen.clicked.connect(self.cmd_hinzufuegen_clicked)
        self.cmd_fertig.clicked.connect(self.cmd_fertig_clicked)

    def cmd_hinzufuegen_clicked(self):
        """Hinzufügen -> Der Benutzer hat sein Wort eingetippt und möchte es dem Set hinzufügen"""

        style_gruen = "color: rgb(0, 85, 0);"
        style_rot = "color: rgb(85, 0, 0);"
        style_schwarz = "color: rgb(0, 0, 0);"

        if self.txt_wort.text() == "" or self.txt_fremdwort.text() == "":
            # Fehler anzeigen
            self.lbl_erfolg.setStyleSheet(style_rot)
            self.lbl_erfolg.setText("Fehler!")
            self.lbl_erfolg.setVisible(True)

            if self.txt_wort.text() == "":
                self.lbl_deutsch.setStyleSheet(style_rot)
                self.lbl_deutsch.setText("Deutsch: (leer!)")
            else:
                self.lbl_deutsch.setStyleSheet(style_schwarz)
                self.lbl_deutsch.setText("Deutsch:")
            if self.txt_fremdwort.text() == "":
                self.lbl_fremdsprache.setStyleSheet(style_rot)
                self.lbl_fremdsprache.setText(f"{self.sprache}: (leer!)")
            else:
                self.lbl_fremdsprache.setStyleSheet(style_schwarz)
                self.lbl_fremdsprache.setText(f"{self.sprache}: ")
            return

        # Cursor erstellen
        cursor = self.dbconn.cursor()

        # Daten aus der Ui laden
        wort = self.txt_wort.text()
        fremdwort = self.txt_fremdwort.text()
        definition = self.txt_definition.text()
        bemerkung = self.txt_bemerkung.text()

        # SQL-Befehl definieren
        sql = """
        INSERT INTO karte (wort, fremdwort, definition, bemerkung, lernfortschritt, markiert, schwierigkeit, set_id)
        VALUES (?, ?, ?, ?, 0, 0, -1, ?) 
        """

        # SQL ausführen
        cursor.execute(sql, (wort, fremdwort, definition, bemerkung, self.set_id))

        # Cursor schliessen und commiten
        cursor.close()
        self.dbconn.commit()

        # UI für neues Wort bereitmachen
        self.txt_wort.setText("")
        self.txt_fremdwort.setText("")
        self.txt_definition.setText("")
        self.txt_bemerkung.setText("")
        self.lbl_deutsch.setStyleSheet(style_schwarz)
        self.lbl_deutsch.setText("Deutsch:")
        self.lbl_fremdsprache.setStyleSheet(style_schwarz)
        self.lbl_fremdsprache.setText(f"{self.sprache}:")

        # Erfolg:
        self.lbl_erfolg.setVisible(True)
        self.lbl_erfolg.setStyleSheet(style_gruen)

        self.wort_zaehler += 1
        if self.wort_zaehler == 1:
            self.lbl_erfolg.setText("Wort hinzugefügt.")
        else:
            self.lbl_erfolg.setText(f"Insgesamt {self.wort_zaehler} Wörter hinzugefügt")


    def cmd_fertig_clicked(self):
        """Fertig -> Der Benutzer ist fertig und möchte den Dialog schliessen."""
        self.close()
