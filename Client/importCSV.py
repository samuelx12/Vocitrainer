# -*- coding: utf-8 -*-
"""
Mp_herunterladen.py
Hier ist das Herunterladen Fenster des Menu Marketplace.
"""

from PyQt5.QtWidgets import *
from res.ui_importCSV import Ui_ImportCSV
import sqlite3
import csv
from explorer_item import ExplorerItem


class ImportCSV(QDialog, Ui_ImportCSV):
    """
    In diesem Fenster befinden sich die Einstellungen, damit danach ein Vociset aus einer Datei importiert werden kann.
    """
    def __init__(self, hauptfenster, *args, obj=None, **kwargs):
        super(ImportCSV, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.hauptfenster = hauptfenster

        self.int_spalteWort.setValue(2)
        self.int_spalteFremdwort.setValue(1)

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # Signale mit Slots verbinden
        self.cmd_abbrechen.clicked.connect(self.cmd_abbrechen_clicked)
        self.cmd_durchsuchen.clicked.connect(self.cmd_durchsuchen_clicked)
        self.txt_pfad.textChanged.connect(self.txt_pfad_textChanged)
        self.cmd_importieren.clicked.connect(self.cmd_importieren_clicked)

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

    def cmd_importieren_clicked(self):
        """
        Der Importvorgang wird mit den eingetragenen Daten gestartet.
        """

        daten = []
        try:
            with open(self.txt_pfad.text(), newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=self.txt_trennzeichen.text())
                for row in csv_reader:
                    daten.append(row)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Vocitrainer - Fehler")
            msg.setText(
                "Fehler beim öffnen bzw. lesen der Datei.\n\n"
                "Bitte überprüfen Sie den angegebenen Pfad und stellen Sie sicher, dass die Datei nicht beschädigt ist."
            )
            msg.exec_()
            return

        try:
            # Verbindung mit der Datenbank aufnehmen.
            self.DBCONN = sqlite3.connect('vocitrainerdb.db')
            self.CURSOR = self.DBCONN.cursor()

            # Wenn kein Name gewählt wurde -> Unbenanntes Set
            if self.txt_name.text() == "" or self.txt_name.text() == " ":
                self.txt_name.setText("Unbenanntes Set")

            # SQL-Query um das Vociset in der Datenbank zu speichern
            query = """
                    INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES (?, ?, ?, 1)
                    """
            self.CURSOR.execute(
                query, [self.txt_name.text(), self.txt_beschreibung.text(), self.cmb_sprache.currentText()]
            )
            importiertes_set_id = self.CURSOR.lastrowid

            query = f"""
            INSERT INTO karte (wort, fremdwort, definition, bemerkung, lernfortschritt, markiert, schwierigkeit, set_id)
            VALUES (?, ?, ?, ?, 0, 0, -1, {importiertes_set_id})
            """
            for zeile in daten:
                if self.int_spalteWort.value() == 0:
                    spalteWort = ""
                else:
                    spalteWort = zeile[self.int_spalteWort.value() - 1]

                if self.int_spalteFremdwort.value() == 0:
                    spalteFremdwort = ""
                else:
                    spalteFremdwort = zeile[self.int_spalteFremdwort.value() - 1]

                if self.int_spalteDefinition.value() == 0:
                    spalteDefinition = ""
                else:
                    spalteDefinition = zeile[self.int_spalteDefinition.value() - 1]

                if self.int_spalteBemerkung.value() == 0:
                    spalteBemerkung = ""
                else:
                    spalteBemerkung = zeile[self.int_spalteBemerkung.value() - 1]

                self.CURSOR.execute(query, [spalteWort, spalteFremdwort, spalteDefinition, spalteBemerkung])
                self.DBCONN.commit()

        except Exception as e:
            # Änderungen rückgängig machen
            self.DBCONN.rollback()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Vocitrainer - Fehler")
            msg.setText(
                "Fehler beim Importieren.\n\n"
                "Bitte überprüfen Sie ihre Eingaben und stellen Sie sicher, dass die Datei nicht beschädigt ist."
            )
            msg.exec_()
            return

        # Fenster schliessen und das neu importierte Set anzeigen.
        importiertes_vociset = ExplorerItem(
            self.txt_name.text(), "vociset", importiertes_set_id, parent=self.hauptfenster.rootNode
        )
        self.hauptfenster.trw_Explorer_doubleClicked(None, importiertes_vociset)

        self.close()
