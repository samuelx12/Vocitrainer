# -*- coding: utf-8 -*-
"""
importQuizlet.py
In diesem Fenster kann man den Link einfügen und den Quizlet import starten.
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from res.ui_importQuizlet import Ui_ImportQuizlet
import sqlite3
from explorer_item import ExplorerItem
from quizlet.export import get_quizlet_set, QuizletExportFehler


class ImportQuizlet(QDialog, Ui_ImportQuizlet):
    """
    In diesem Fenster befinden sich die Einstellungen, damit danach ein Vociset aus einer Datei importiert werden kann.
    """
    def __init__(self, hauptfenster, *args, **kwargs):
        super(ImportQuizlet, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.hauptfenster = hauptfenster
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Hilfebutton ausblenden

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # Signale mit Slots verbinden
        self.cmd_abbrechen.clicked.connect(self.cmd_abbrechen_clicked)
        self.cmd_importieren.clicked.connect(self.cmd_importieren_clicked)

    def cmd_abbrechen_clicked(self) -> None:
        """Abbrechen wurde geklickt -> Fenster schliessen"""
        self.close()

    def cmd_importieren_clicked(self):
        """
        Der Importvorgang wird mit den eingetragenen Daten gestartet.
        """

        link = self.txt_link.text()

        try:
            titel, daten = get_quizlet_set(link)
        except QuizletExportFehler:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Vocitrainer - Fehler")
            msg.setText(
                "Beim Importieren des Quizlet-Sets ist ein Fehler aufgetreten.\n"
                "Überprüfe doch, ob der Link korrekt ist und die neueste Version des Vocitrainers installiert ist."
            )
            msg.exec_()
            return

        try:
            # Verbindung mit der Datenbank aufnehmen.
            self.DBCONN = sqlite3.connect('vocitrainerdb.db')
            self.CURSOR = self.DBCONN.cursor()

            # SQL-Query um das Vociset in der Datenbank zu speichern
            query = """
                    INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES (?, ?, ?, 1)
                    """
            self.CURSOR.execute(
                query, [titel, "", self.cmb_sprache.currentText()]
            )

            importiertes_set_id = self.CURSOR.lastrowid

            if self.box_definition.isChecked():
                query = """
                    INSERT INTO karte (wort, fremdwort, definition, bemerkung, lernfortschritt, markiert, schwierigkeit, set_id)
                    VALUES ('', ?, ?, '', 0, 0, -1, ?)
                """
            else:
                query = """
                    INSERT INTO karte (wort, fremdwort, definition, bemerkung, lernfortschritt, markiert, schwierigkeit, set_id)
                    VALUES (?, ?, '', '', 0, 0, -1, ?)
                """
            for zeile in daten:
                spalteWort = zeile[1]
                spalteFremdwort = zeile[0]
                if self.box_vertauschen.isChecked():
                    spalteWort, spalteFremdwort = spalteFremdwort, spalteWort

                self.CURSOR.execute(query, [spalteWort, spalteFremdwort, importiertes_set_id])
                self.DBCONN.commit()

        except Exception:
            # Änderungen rückgängig machen
            self.DBCONN.rollback()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Vocitrainer - Fehler")
            msg.setText(
                "Beim Speichern der importierten Vokablen ist ein Fehler aufgetreten."
            )
            msg.exec_()
            self.DBCONN.close()
            return

        self.DBCONN.close()

        # Fenster schliessen und das neu importierte Set anzeigen.
        importiertes_vociset = ExplorerItem(
            titel, "vociset", importiertes_set_id, parent=self.hauptfenster.rootNode
        )
        self.hauptfenster.trw_Explorer_doubleClicked(None, importiertes_vociset)

        self.close()
