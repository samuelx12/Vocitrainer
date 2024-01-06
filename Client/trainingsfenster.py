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
from trainingscontroller import TC_Einfach, TC_Intelligent, TrainingFertig
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

    def __init__(self, daten: list, sprache: str, definition_lernen: bool, *args, **kwargs):
        super(Trainingsfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Vocitrainer")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.training_beendet = False

        # Sprache gleich für alles Einstellen:
        self.sprache: str = sprache
        self.f_lbl_fremdsprache.setText(self.sprache)
        self.a_lbl_fremdsprache_beschreibung.setText(self.sprache)
        self.z_lbl_fremdsprache_beschreibung.setText(self.sprache)

        # Mit Definition lernen falls vorhanden einstellen
        self.definition_lernen: bool = definition_lernen

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4 / 12), int(hoehe * 3 / 8), int(breite * 1 / 3), int(hoehe * 1 / 6))

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
        Eine mögliche Verbesserung wäre hier, dass zum Beispiel bei gegebener Loesung
        "to listen (verb)" auch einfach "to listen" als Antwort akzeptiert wird.
        """
        return antwort == loesung

    def phase1(self):
        """
        In dieser Phase werden die Daten vom Controller geladen.
        Dann wird entweder nach dem Voci gefragt oder das neue Wort wird gezeigt.
        """

        # --- Kontroller nach dem nächsten Voci fragen ---
        try:
            self.aktive_karte, karte_zeigen = self.controller.frage()
        except TrainingFertig:
            self.training_beendet = True
            self.close()
            return

        if karte_zeigen:
            # --- Zeigeseite laden ---
            self.z_lbl_deutsch_wort.setText(self.aktive_karte.wort)
            self.z_lbl_fremdsprache_wort.setText(self.aktive_karte.fremdwort)

            # Allenfalls Definition zeigen
            if self.aktive_karte.bemerkung == "":
                self.z_lbl_definition_beschreibung.setVisible(False)
                self.z_lbl_definition_wort.setVisible(False)
            else:
                self.z_lbl_definition_beschreibung.setVisible(True)
                self.z_lbl_definition_wort.setVisible(True)
                self.z_lbl_definition_wort.setText(self.aktive_karte.definition)

            # Allenfalls Bemerkung zeigen
            if self.aktive_karte.bemerkung == "":
                self.z_lbl_bemerkung_beschreibung.setVisible(False)
                self.z_lbl_bemerkung_wort.setVisible(False)
            else:
                self.z_lbl_bemerkung_beschreibung.setVisible(True)
                self.z_lbl_bemerkung_wort.setVisible(True)
                self.z_lbl_bemerkung_wort.setText(self.aktive_karte.bemerkung)

            # Zeigeseite anzeigen
            self.stackedWidget.setCurrentIndex(2)
        else:
            # --- Frageseite laden ---
            if self.definition_lernen and self.aktive_karte.definition != "":
                self.f_lbl_deutsch_beschreibung.setText("Definition:")
                self.f_lbl_deutsch_wort.setText(self.aktive_karte.definition)
            else:
                self.f_lbl_deutsch_beschreibung.setText("Deutsch:")
                self.f_lbl_deutsch_wort.setText(self.aktive_karte.wort)

            # Eingabefeld leeren
            self.f_txt_fremdsprache.setText("")

            # Frageseite anzeigen
            self.stackedWidget.setCurrentIndex(0)

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

        # --- Antwortsseite anzeigen ---
        self.stackedWidget.setCurrentIndex(1)

    def closeEvent(self, event: QCloseEvent):
        """
        Überschreiben der closeEvent-Methode, um das Schließen des Fensters zu überwachen.
        """

        if self.training_beendet:
            # Das Training ist fertig
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Vocitrainer")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText(
                "Das Training ist beendet. Gratulation!"
            )
            event.accept()
            msg.exec_()

        else:
            # Der Benutzer will das Training vorzeitig beenden.
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
        """PRÜFEN GEKLICKT"""
        # Phase 2 starten
        self.phase2()

    def f_cmd_abbrechen_clicked(self):
        """ABBRECHEN GEKLICKT"""
        # Fenster schliessen
        self.close()

    # ----------------------------------
    # ---------- Antwortseite ----------
    # ----------------------------------

    def a_cmd_weiter_clicked(self):
        """WEITER GEKLICKT"""
        # Phase 1 wieder einleiten
        self.phase1()

    def a_cmd_abbrechen_clicked(self):
        """ABBRECHEN GEKLICKT"""
        # Fenster schliessen
        self.close()

    # ---------------------------------------------
    # ---------- Zeigeseite (Neues Wort) ----------
    # ---------------------------------------------

    def z_cmd_weiter_clicked(self):
        """WEITER GEKLICKT"""
        # Phase 1 aufrufen
        self.phase1()

    def z_cmd_abbrechen_clicked(self):
        """ABBRECHEN GEKLICKT"""
        # Fenster schliessen
        self.close()
