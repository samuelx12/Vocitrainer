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
from rich import print as rprint


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
        self.CURSOR = self.DBCONN.cursor()
        self.controller_typ = controller_typ

        # Einstellung Fokusmodus und Definition lernen laden
        try:
            config = ConfigObj("settings.ini")
            self.definition_lernen = bool(int(config['Lernen']['definitionLernen']))
            self.fokusmodus_aktiv = bool(int(config['Lernen']['fokusmodus']))
        except:
            self.definition_lernen: bool = False
            self.fokusmodus_aktiv = False

        # Einstellung: Sprache gleich für alles Einstellen:
        self.sprache: str = sprache
        self.f_lbl_fremdsprache.setText(self.sprache + ":")
        self.a_lbl_fremdsprache_beschreibung.setText(self.sprache + ":")
        self.z_lbl_fremdsprache_beschreibung.setText(self.sprache + ":")

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
        self.f_cmd_markiert.clicked.connect(self.f_cmd_markiert_clicked)
        self.a_cmd_weiter.clicked.connect(self.a_cmd_weiter_clicked)
        self.a_cmd_abbrechen.clicked.connect(self.a_cmd_abbrechen_clicked)
        self.a_cmd_trotzdemRichtig.clicked.connect(self.a_cmd_trotzdemRichtig_clicked)
        self.a_cmd_trotzdemFalsch.clicked.connect(self.a_cmd_trotzdemFalsch_clicked)
        self.a_cmd_markiert.clicked.connect(self.a_cmd_markiert_clicked)
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

        # Falls aber Fokusmodus, Schwierigkeit sowieso aus:
        if self.fokusmodus_aktiv:
            self.schwierigkeit_zeigen = False

        # Erste Frage laden
        self.phase1()

    @staticmethod
    def wortbereinigung(wort: str) -> str:
        """Bereinig das Wort: Löscht überflüssige Leerzeichen."""

        # Entferne überflüssige Leerzeichen
        bereinigtes_wort = " ".join(wort.split())

        return bereinigtes_wort

    def antwort_pruefen(self, antwort: str, loesung: str, karte_id: int) -> (bool, bool):
        """
        Hier wird die Antwort überprüft.
        Eine mögliche Verbesserung wäre hier, dass zum Beispiel bei gegebener Loesung
        "to listen (verb)" auch einfach "to listen" als Antwort akzeptiert wird.
        :return: ist_korrekt, ist_zweitloesung
        """
        def klammerentfernung(text: str) -> str:
            """Entfernt den Teil des Strings, der sich in Klammern befindet."""

            # Finde die Indexe der öffnenden und schließenden Klammern
            opening_bracket = text.find('(')
            closing_bracket = text.find(')')

            # Überprüfe, ob sowohl öffnende als auch schließende Klammern gefunden wurden
            if opening_bracket != -1 and closing_bracket != -1:
                # Entferne den Teil des Strings zwischen den Klammern und die Klammern selbst
                bereinigter_text = text[:opening_bracket] + text[closing_bracket + 1:]
            else:
                # Wenn keine Klammern gefunden wurden, bleibt der Text unverändert
                bereinigter_text = text

            return self.wortbereinigung(bereinigter_text.strip())

        # Bereinigung von Loesung und antwort
        antwort = self.wortbereinigung(antwort)
        loesung = self.wortbereinigung(loesung)

        if antwort == loesung:
            # Antwort stimmt exakt
            return True, False

        # --- Wenns weiter geht, ist die Sache komplizierter (oder falsch) ---

        # Zweitlösungen laden
        sql = """SELECT fremdwort, korrekt FROM loesung WHERE karte_id = ?"""
        self.CURSOR.execute(sql, (karte_id,))
        zweitloesungen = self.CURSOR.fetchall()

        # Lösungen auftrennen und sortieren
        richtige_zweitloesungen = []
        falsche_zweitloesungen = []
        for zweitloesung in zweitloesungen:
            if bool(zweitloesung[1]):
                richtige_zweitloesungen.append(zweitloesung[0])
            else:
                falsche_zweitloesungen.append(zweitloesung[0])

        print("Zweitloesungen:")
        rprint(richtige_zweitloesungen, falsche_zweitloesungen)

        klammerlose_loesung = klammerentfernung(loesung)
        if antwort == klammerlose_loesung and klammerlose_loesung not in falsche_zweitloesungen:
            # Ohne die Klammern richtig und in den Zweitlösungen ist nichts anderes registriert.
            # Gilt nicht als Zweitlösung
            return True, False

        if antwort in richtige_zweitloesungen:
            # Antwort ist eine richtige Zweitlösung
            return True, True

        # Sonst ist die lösung Falsch
        return False, False

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
            self.f_cmd_markiert.setChecked(self.aktive_karte.markiert)
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

        return

    def phase2(self):
        """
        In dieser Phase wird die Antwort von der Frage gezeigt.
        (Falls zuvor ein Voci gezeigt wurde, wird diese Methode gar nicht erst ausgeführt.
        """
        # --- Antwort überprüfen ---
        user_antwort = self.f_txt_fremdsprache.text()
        antwort_korrekt, ist_zweitloesung = self.antwort_pruefen(
            user_antwort, self.aktive_karte.fremdwort, self.aktive_karte.ID)

        # --- Kontroller soll über das Resultat informiert werden ---
        self.aktive_karte = self.controller.antwort(antwort_korrekt)

        self.antwortseite_laden(antwort_korrekt, user_antwort, ist_zweitloesung)

        # --- Antwortsseite anzeigen ---
        self.stackedWidget.setCurrentIndex(1)

    def neubewertung(self, trotzdemWahrheitswert: bool):
        """
        Funktion um eine Neubewertung vorzunehmen.
        Dabei wird die neue Lösung auch in der Datenbank gespeichert.
        """
        user_antwort = self.f_txt_fremdsprache.text()
        self.aktive_karte = self.controller.antwort(trotzdemWahrheitswert, neubewertung=True)

        # Allenfalls dazu existierende Lösungen oder nicht Lösungen löschen
        query = """
            DELETE FROM loesung WHERE fremdwort = ? AND karte_id = ?
        """
        self.CURSOR.execute(query, (user_antwort, self.aktive_karte.ID))

        # Neue Lösung erstellen
        query = """
            INSERT INTO loesung (karte_id, korrekt, fremdwort) VALUES (?, ?, ?)
        """
        self.CURSOR.execute(query, (self.aktive_karte.ID, int(trotzdemWahrheitswert), user_antwort))
        self.DBCONN.commit()

        self.antwortseite_laden(trotzdemWahrheitswert, user_antwort, ist_zweitloesung=True)

        return

    def antwortseite_laden(self, antwort_korrekt: bool, benutzer_antwort: str, ist_zweitloesung: bool = False):
        """
        Teil von phase2 aber ausgelagert um Neubewertungen möglich zu machen
        """

        # --- Antwortsseite laden ---
        # Deutsches Wort:
        self.a_lbl_deutsch_wort.setText(self.aktive_karte.wort)

        # Markier Button
        self.a_cmd_markiert.setChecked(self.aktive_karte.markiert)

        # Fremdwort mit allfälliger Korrektur
        if antwort_korrekt and ist_zweitloesung:
            self.a_lbl_fremdsprache_wort.setText(benutzer_antwort)
        else:
            self.a_lbl_fremdsprache_wort.setText(self.aktive_karte.fremdwort)
        self.a_lbl_deineAntwort_beschreibung.setVisible(not antwort_korrekt)
        self.a_lbl_deineAntwort_wort.setVisible(not antwort_korrekt)
        self.a_lbl_trotzdemFalsch.setVisible(antwort_korrekt and ist_zweitloesung)
        self.a_cmd_trotzdemFalsch.setVisible(antwort_korrekt and ist_zweitloesung)
        self.a_lbl_trotzdemRichtig.setVisible(not antwort_korrekt)
        self.a_cmd_trotzdemRichtig.setVisible(not antwort_korrekt)
        if antwort_korrekt:
            pass
        else:
            self.a_lbl_deineAntwort_wort.setText(benutzer_antwort)

        self.a_lbl_deutsch_beschreibung.setText("Deutsch:")
        # Allenfalls Definition zeigen
        if self.aktive_karte.definition == "":
            self.a_lbl_definition_beschreibung.setVisible(False)
            self.a_lbl_definition_wort.setVisible(False)
        else:
            if self.definition_lernen:
                # Allenfalls bei verfübarer Funktion, diese oben anzeigen.
                self.a_lbl_deutsch_beschreibung.setText("Definition:")
                self.a_lbl_deutsch_wort.setText(self.aktive_karte.definition)

                if self.aktive_karte.wort == "":
                    self.a_lbl_definition_beschreibung.setVisible(False)
                    self.a_lbl_definition_wort.setVisible(False)
                else:
                    self.a_lbl_definition_beschreibung.setVisible(True)
                    self.a_lbl_definition_beschreibung.setText("Deutsch:")
                    self.a_lbl_definition_wort.setVisible(True)
                    self.a_lbl_definition_wort.setText(self.aktive_karte.wort)
            else:
                self.a_lbl_definition_beschreibung.setVisible(True)
                self.a_lbl_definition_beschreibung.setText("Definition:")
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

        # Fokusmodus umsetzen falls aktiviert
        self.fokusmodus()

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
            msg.button(QMessageBox.Yes).setText("Ja")
            msg.button(QMessageBox.No).setText("Nein")
            antwort = msg.exec_()

            if antwort == QMessageBox.Yes:
                self.training_beenden()
                event.accept()  # Fenster wird geschlossen.
            else:
                event.ignore()  # Sonst muss nichts passieren

    def fokusmodus(self):
        """
        Diese Funktion blendet einfach alle Bemerkungs und Definitions Labels aus.
        Zwar könnte man das alles schon vorher regeln, aber es bringt so keine Performance Einbussen und
        macht den Code viel Lesbarer, da if-Konstrukte wegfallen.
        Dafür muss jedoch self.fokusmodus True sein.
        """
        if not self.fokusmodus_aktiv:
            return
        
        self.a_lbl_definition_wort.setVisible(False)
        self.a_lbl_definition_beschreibung.setVisible(False)
        self.a_lbl_bemerkung_wort.setVisible(False)
        self.a_lbl_bemerkung_beschreibung.setVisible(False)

        self.z_lbl_bemerkung_wort.setVisible(False)
        self.z_lbl_bemerkung_beschreibung.setVisible(False)

    def markieren(self, markiert: bool):
        """Das aktuelle Wort (ent)markieren"""
        id = self.aktive_karte.ID

        sql = """UPDATE karte SET markiert=? WHERE karte_id=?"""
        self.CURSOR.execute(sql, (int(markiert), id))

    def training_beenden(self):
        """Wenn das Training beendet werden soll, wird diese Funktion aufgerufen."""
        self.CURSOR.close()
        # self.DBCONN.close()

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

    def f_cmd_markiert_clicked(self):
        """Markieren Button geklickt"""
        self.markieren(self.f_cmd_markiert.isChecked())

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

    def a_cmd_trotzdemRichtig_clicked(self):
        """Trotzdem Richtig geklickt"""
        self.neubewertung(trotzdemWahrheitswert=True)

    def a_cmd_trotzdemFalsch_clicked(self):
        """Trotzdem Falsch geklickt"""
        self.neubewertung(trotzdemWahrheitswert=False)

    def a_cmd_markiert_clicked(self):
        """Markieren Button geklickt"""
        self.markieren(self.a_cmd_markiert.isChecked())

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
