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
from res.ui_trainingsfenster import Ui_Trainingsfenster
from trainingscontroller import TC_Einfach, TC_Intelligent, TrainingFertig
from karte_tuple import Karte
from sqlite3 import Connection
from typing import List
from configobj import ConfigObj
import ressources_rc


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

    def __init__(
            self,
            daten: List[Karte],
            sprache: str,
            controller_typ: str,
            dbconn: Connection,
            *args,
            **kwargs
    ):
        super(Trainingsfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Vocitrainer")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.training_beendet = False
        self.schliessen_ohne_kommentar = False
        self.oeffnen = True
        self.DBCONN = dbconn
        self.controller_typ = controller_typ

        try:
            config = ConfigObj("settings.ini")
            self.definition_lernen = bool(int(config['Lernen']['definitionLernen']))
        except:
            self.definition_lernen: bool = False

        # Einstellung: Sprache gleich für alles Einstellen:
        self.sprache: str = sprache
        self.f_lbl_fremdsprache.setText(self.sprache + ":")
        self.a_lbl_fremdsprache_beschreibung.setText(self.sprache + ":")
        self.z_lbl_fremdsprache_beschreibung.setText(self.sprache + ":")

        # Einstellung: Schwierigkeit anzeigen
        self.schwierigkeit_zeigen = True

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
        if self.controller_typ == "einfach":
            self.controller = TC_Einfach(daten)
            self.schwierigkeit_zeigen = False

        elif self.controller_typ == "intelligent":
            try:
                self.controller = TC_Intelligent(daten, self.DBCONN)
            except TrainingFertig:
                # Es gibt gar nichts zu lernen
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowIcon(QIcon(":/icons/res/icons/warning_FILL0_wght400_GRAD0_opsz24.svg"))
                msg.setWindowTitle("Vocitrainer")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setText(
                    "Du kennst schon alle Wörter! Umso besser.\n\n" +
                    "Wenn du die Wörter weiter üben willst, kannst du das mit dem einfachen Modus tun.\n\n" +
                    "Ansonsten musst du dein Fortschritt für dieses Set zurücksetzen."
                )
                self.oeffnen = False
                msg.exec_()
                return

            self.schwierigkeit_zeigen = True

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

    def zeige_schwierigkeit(self, karte: Karte, seite: str):
        """
        Zeigt die Schwierigkeit der Karte auf, falls die Einstellung dazu entsprechend ist.
        :param karte: Welcher Karte Schwierigkeit
        :param seite: Auf welcher Seite
        :return:
        """

        if seite == "f":
            schwierigkeits_label = self.f_lbl_schwierigkeit
        elif seite == "a":
            schwierigkeits_label = self.a_lbl_schwierigkeit
        else:
            return

        # Wenn Einstellung nicht aktiv ist:
        if not self.schwierigkeit_zeigen:
            schwierigkeits_label.setVisible(False)
            return

        # Verbleibende Abfragen berechnen
        # Es scheint kompliziert, aber wenn man sich eine Tabelle macht und sich die Sache genau anschaut
        # macht der folgende Rechenweg Sinn.
        ftoleranz = self.controller.fehlertoleranz

        if karte.schwierigkeit_training % ftoleranz == 0:
            summand = ftoleranz
        else:
            summand = abs(karte.schwierigkeit_training % ftoleranz)

        verbleibend = (karte.schwierigkeit_training + summand) // ftoleranz

        # Farbe und Text bestimmen
        if karte.schwierigkeit_max == -1:
            level = "Unbekannt"
            farbe = "rgb(80, 80, 80)"
            verbleibend = 1
        elif karte.schwierigkeit_max == 0:
            level = "Einfach"
            farbe = "rgb(0, 85, 0)"
        elif karte.schwierigkeit_max == 1:
            level = "Mittelmässig"
            farbe = "rgb(198, 132, 0)"
        elif karte.schwierigkeit_max == 2:
            level = "Schwer"
            farbe = "rgb(170, 0, 0)"
        else:
            level = "Sehr schwer"
            farbe = "rgb(255, 0, 0)"

        schwierigkeits_label.setText(level + f" (Min. verbleibende Abfragen: {verbleibend})")
        schwierigkeits_label.setStyleSheet(
            f"""
            color: {farbe};
            font: 75 13pt "MS Shell Dlg 2";
            """
        )
        schwierigkeits_label.setVisible(True)

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

            # Schwierigkeit anzeigen
            self.zeige_schwierigkeit(self.aktive_karte, "f")

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
        self.aktive_karte = self.controller.antwort(antwort_korrekt)

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

        # Schwierigkeit anzeigen
        self.zeige_schwierigkeit(self.aktive_karte, "a")

        # --- Antwortsseite anzeigen ---
        self.stackedWidget.setCurrentIndex(1)

    def closeEvent(self, event: QCloseEvent):
        """
        Überschreiben der closeEvent-Methode, um das Schließen des Fensters zu überwachen.
        """

        if self.schliessen_ohne_kommentar:
            event.accept()
            return

        if self.training_beendet:
            # Das Training ist fertig
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon(':/icons/res/icons/info_FILL0_wght400_GRAD0_opsz24.svg'))
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
            msg.setWindowIcon(QIcon(':/icons/res/icons/help_FILL0_wght400_GRAD0_opsz24.svg'))
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
