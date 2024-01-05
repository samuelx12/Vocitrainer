# -*- coding: utf-8 -*-
"""
trainingsfenster.py
Diese Datei enthält eigentlich nur die Klasse Trainingsfenster, welche von QMainWindow erbt. Das Hauptfenster ist
das erste Fenster, welches aufgeht. Das Programm läuft weiter, wenn Signale auftreten, welche mit einem Slot (Funktion)
verbunden wurden (Qt-Konzept)
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Client.res.qt.ui_trainingsfenster import Ui_Trainingsfenster
from trainingscontroller import TC_Einfach
from karte_tuple import Karte


class Trainingsfenster(QDialog, Ui_Trainingsfenster):
    """
    Trainingsfenster
    Das Trainingsfenster hat im Zentrum ein 'Stacked_Widget' mit drei Seiten:
        0 -> Frageseite: Hier wird ein Eingabefenster gezeigt, in dem das Wort eingegeben werden muss.
        1 -> Antwortseite: Hier wird gezeigt, ob die letzte Frage richtig beantwortet wurde.
        2 -> Zeigeseite: Wenn im Intelligenten Modus ein neues Wort hinzu kommt, wird es mit dieser Seite gezeigt.

    Die Slots der Seiten sind in der Klasse unten zur besseren Lesbarkeit auch schön in dieser Reihenfolge getrennt.
    -------
    Das Lernen geht immer in 2 Phasen vor sich:
        Phase 1:
            Daten laden
            Frage stellen oder Voci zeigen
        Phase 2:
            Falls in Phase 1 eine Frage gestellt wurde, die Antwort anzeigen.
    """
    def __init__(self, daten, sprache, *args, **kwargs):
        super(Trainingsfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Training")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        # Sprache gleich für alles Einstellen:
        self.sprache = sprache
        self.f_lbl_fremdsprache.setText(self.sprache)
        self.a_lbl_fremdsprache_beschreibung.setText(self.sprache)
        self.z_lbl_fremdsprache_beschreibung.setText(self.sprache)

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # self.setCentralWidget(self.stackedWidget)
        self.stackedWidget.setCurrentIndex(0)

        # Signale mit Slots verbinden
        self.f_cmd_pruefen.clicked.connect(self.f_cmd_pruefen_clicked)
        self.f_cmd_abbrechen.clicked.connect(self.f_cmd_abbrechen_clicked)
        self.a_cmd_weiter.clicked.connect(self.a_cmd_weiter_clicked)
        self.a_cmd_abbrechen.clicked.connect(self.a_cmd_abbrechen_clicked)
        self.z_cmd_weiter.clicked.connect(self.z_cmd_weiter_clicked)
        self.z_cmd_abbrechen.clicked.connect(self.z_cmd_abbrechen_clicked)

        self.setStyleSheet(
            """font: 14pt "MS Shell Dlg 2";"""
        )

        # Training Controller laden
        self.controller = TC_Einfach(daten)

        # Erste Frage laden
        self.phase1()

    @staticmethod
    def antwort_pruefen(antwort, loesung) -> bool:
        """
        Hier wird die Antwort überprüft.
        Eine mögliche Erweiterung wäre hier,
        dass zum Beispiel bei gegebener Loesung "to listen (verb)" auch einfach "to listen" als Antwort akzeptiert wird.
        """
        return antwort == loesung

    def phase1(self):
        """
        In dieser Phase werden die Daten vom Controller geladen.
        Dann wird entweder nach dem Voci gefragt oder das neue Wort wird gezeigt.
        """
        self.aktive_karte = self.controller.frage()

        self.f_txt_fremdsprache.setText("")
        self.f_lbl_deutsch_wort.setText(self.aktive_karte.wort)

    def phase2(self):
        """
        In dieser Phase wird die Antwort von der Frage gezeigt.
        (Falls zuvor ein Voci gezeigt wurde, wird diese Methode gar nicht erst ausgeführt.
        """
        # --- Antwort überprüfen ---
        user_antwort = self.f_txt_fremdsprache.text()
        antwort_korrekt = self.antwort_pruefen(user_antwort, self.aktive_karte.fremdwort)

        # --- Kontroller soll über das Resultat informiert werden ---
        self.controller.antwort(antwort_korrekt)

        # --- Antwortsseite laden ---
        # Deutsches Wort:
        self.a_lbl_deutsch_wort.setText(self.aktive_karte.wort)

        # Fremdwort mit allfälliger Korrektur
        self.a_lbl_fremdsprache_wort.setText(self.aktive_karte.fremdwort)
        if antwort_korrekt:
            self.a_lbl_deineAntwort_beschreibung.setVisible(False)
            self.a_lbl_deineAntwort_wort.setVisible(False)
        else:
            self.a_lbl_deineAntwort_beschreibung.setVisible(True)
            self.a_lbl_deineAntwort_wort.setVisible(True)
            self.a_lbl_deineAntwort_wort.setText(user_antwort)

        # Allenfalls Definition zeigen
        if self.aktive_karte.bemerkung == "":
            self.a_lbl_definition_beschreibung.setVisible(False)
            self.a_lbl_definition_wort.setVisible(False)
        else:
            self.a_lbl_definition_beschreibung.setVisible(True)
            self.a_lbl_definition_wort.setVisible(True)
            self.a_lbl_definition_wort.setText(self.aktive_karte.definition)

        # Allenfalls Bemerkung zeigen
        if self.aktive_karte.bemerkung == "":
            self.a_lbl_bemerkung_beschreibung.setVisible(False)
            self.a_lbl_bemerkung_wort.setVisible(False)
        else:
            self.a_lbl_bemerkung_beschreibung.setVisible(True)
            self.a_lbl_bemerkung_wort.setVisible(True)
            self.a_lbl_bemerkung_wort.setText(self.aktive_karte.bemerkung)


    def closeEvent(self, event: QCloseEvent):
        """
        Überschreiben der closeEvent-Methode, um das Schließen des Fensters zu überwachen.
        """

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Vocitrainer")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setText(
            "Willst du das Training beenden?"
        )
        antwort = msg.exec_()

        if antwort == QMessageBox.Yes:
            self.training_beenden()
            event.accept()  # Fenster wird geschlossen.
        else:
            event.ignore()  # Sonst muss nichts passieren

    def training_beenden(self):
        """Wenn das Training beendet werden soll, wird diese Funktion aufgerufen."""
        pass

    # --------------------------------
    # ---------- FRAGESEITE ----------
    # --------------------------------

    def f_cmd_pruefen_clicked(self):
        """Frageseite: PRÜFEN GEKLICKT"""

        antwort_korrekt = self.antwort_pruefen(self.f_txt_fremdsprache.text())

        antwort = self.controller.antwort(self.f_txt_fremdsprache.text())
        self.a_lbl_deutsch_wort.setText(antwort[0][1])
        self.a_lbl_fremdsprache_wort.setText(antwort[0][2])
        self.a_lbl_deutsch_beschreibung.setText(str(antwort[1]))
        if antwort[1]:
            self.a_lbl_fremdsprache_wort.setStyleSheet(
                """
                background-color: rgb(197, 225, 196);
                border: 3px solid;
                border-radius: 3px;
                border-color: rgb(197, 225, 196);
                """
            )
        else:
            self.a_lbl_fremdsprache_wort.setStyleSheet(
                """
                background-color: rgb(225, 171, 171);
                border: 3px solid;
                border-radius: 3px;
                border-color: rgb(225, 171, 171);
                """
            )
        self.stackedWidget.setCurrentIndex(1)

    def f_cmd_abbrechen_clicked(self):
        """ABBRECHEN (Frageseite) GEKLICKT"""
        self.close()

    # ----------------------------------
    # ---------- Antwortseite ----------
    # ----------------------------------

    def a_cmd_weiter_clicked(self):
        """WEITER GEKLICKT"""
        self.phase1()
        self.stackedWidget.setCurrentIndex(0)

    def a_cmd_abbrechen_clicked(self):
        """ABBRECHEN (Antwortseite) GEKLICKT"""
        self.close()

    # ---------------------------------------------
    # ---------- Zeigeseite (Neues Wort) ----------
    # ---------------------------------------------

    def z_cmd_weiter_clicked(self):
        """WEITER GEKLICKT"""
        pass

    def z_cmd_abbrechen_clicked(self):
        """ABBRECHEN (Zeigenseite) GEKLICKT"""
        self.close()
