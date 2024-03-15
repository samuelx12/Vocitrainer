# -*- coding: utf-8 -*-
"""
trainingscontroller.py
Hierhin kommen die Kontroll-Klassen für das Training
"""
from PyQt5.QtGui import QColor

from karte_tuple import Karte
from typing import Iterable
from rich import print as rprint
from sqlite3 import Connection
from configobj import ConfigObj
import copy


class TC_Einfach:
    """
    Ein einfacher Trainingscontroller, der Wörter immer wiederholt, bis alle einmal richtig geschrieben wurden.
    """
    def __init__(self, lernliste):
        self.lernliste = lernliste
        self.groesse_urlernliste = len(self.lernliste)
        self.i = 0  # Counter
        self.altes_i = 0
        self.aktuelles_i = 0
        self.alte_lernliste = self.lernliste
        self.resultat = False

    def frage(self) -> (Karte, bool):
        """
        Gibt die Frage zurück
        :return: 1. Kartendaten, 2. Ob die Karte gezeigt oder danach gefragt werden soll.
        """
        try:
            neues_wort = self.lernliste[self.i]
        except IndexError:
            # Wenn das Training fertig ist wird das über die Exception gemeldet
            raise TrainingFertig

        self.aktuelles_i = self.i

        return neues_wort, False

    def antwort(self, resultat: bool, neubewertung: bool = False):
        """
        Mit dieser Funktion wird der Trainingscontroller informiert, ob die Frage richtig beantwortet wurde
        """
        self.resultat = resultat
        if neubewertung:
            self.lernliste = copy.deepcopy(self.alte_lernliste)
            self.i = self.altes_i
        else:
            self.alte_lernliste = copy.deepcopy(self.lernliste)
            self.altes_i = self.i

        karte = self.lernliste[self.i]

        if resultat:
            self.lernliste.pop(self.i)  # Gelerntes Wort aus der Liste entfernen
        else:
            self.i += 1  # Wortcounter weiter stellen

        # Wenn beim letzten Wort -> Counter wieder auf 0
        if self.i + 1 > len(self.lernliste):
            self.i = 0

        # Wenn kein Wort mehr übrig
        if len(self.lernliste) == 0:
            pass

        return karte

    def fortschritt(self) -> list:
        """
        Gibt eine Tupel zurück, in der alle Daten enthalten sind, um den Fortschrittsbalken zu zeichnen.
        """
        fortschritts_daten = []

        # Grüner Balken für gelernte Wörter
        anteil_gelernte = (self.groesse_urlernliste - len(self.lernliste)) / self.groesse_urlernliste
        farbe_gelernte = QColor(197, 225, 196)  # Sanftes Grün
        eintrag_gelernte = (farbe_gelernte, 0, anteil_gelernte)
        fortschritts_daten.append(eintrag_gelernte)

        # Roter Balken für ungelernte Wörter
        farbe_ungelernte = QColor(225, 171, 171)  # Sanftes Rot
        eintrag_ungelernte = (farbe_ungelernte, anteil_gelernte, 1)
        fortschritts_daten.append(eintrag_ungelernte)

        # Gelb für das gerade Lernende Wort
        beginn_lernende = anteil_gelernte + self.aktuelles_i / self.groesse_urlernliste
        schluss_lernende = anteil_gelernte + (self.aktuelles_i + 1) / self.groesse_urlernliste
        farbe_lernende = QColor(252, 186, 3)  # Gelb
        eintrag_lernende = (farbe_lernende, beginn_lernende, schluss_lernende)
        fortschritts_daten.append(eintrag_lernende)

        return fortschritts_daten


# noinspection PyUnresolvedReferences
class TC_Intelligent:
    """
    Hier steht der Controller für den Intelligenten Lernmodus.
    Über die Algorithmik und die psychologischen Hintergrundgedanken steht genaueres
    in eigenen Dateien im "Dokumentation"-Ordner und im Kaptiel der schriftlichen Arbeit

    Schwierigkeit: Es gibt zwei Schwierigkeiten.

    Schwierigkeit_Training
        - Schwierigkeit_Training zählt, wie häufig das Voci falsch beantwortet wurde.
        - Wenn es jedoch richtig geschriebe wird verringert sich dieser Wert wieder
        - Das Wort gilt dann als gelernt, wenn die Schwierigkeit_Training ~0 erreicht
        - Schwierigkeit Training existiert nur für die Laufzeit des Trainings

    Schwierigkeit_Max
        - Im Gegensatz zu Schwierigkeit_Training wird Schwierigkeit_Max in der Datenbank festgehalten.
        - Das Ziel ist, das der Wert die Schwierigkeit des Wortes für den Benutzer zeigt
        - 0=Einfach, 1=Mittelmässig, 2=Schwer, 3=Sehr Schwer
        - Die Schwierigkeit_Max ist die maximale im Training erreichte Schwierigkeit durch die Fehlertoleranz

    Fehlertoleranz
        - Die Fehlertoleranz bestimmt, ab wie vielen falschen Antworten, das Wort eine Schwierigkeitsstufe höher rückt
        - Angenommen, die Fehlertoleranz ist 2: Nach zwei Falschen Antworten, muss das Wort zusätzlich einmal
          neu geschrieben werden, ausserdem gilt es ab 2 Antworten als "mittelmässig" schwer
        - Eine hohe Fehlertoleranz ist für die Leute geignet, welche eher lange brauchen bis sie das Wort können bzw.
          viele Flüchtigkeitsfehler machen: So werden die Wörter für sie nicht schwieriger eingestuft als sie
          eigentlich sind.
        - Die Standart-Fehlertoleranz ist 2
    """
    def __init__(self, lernliste: Iterable[Karte], dbconn: Connection):
        # DB Connection speichern
        self.DBCONN = dbconn

        # Variable ob Updates auch in die Datenbank geschrieben werden sollen
        self.training_speichern = True

        # Countervariable
        self.i = 0
        self.altes_i = 0
        self.gespeichert_aenderungen = []

        try:
            config = ConfigObj('settings.ini')
            # Einstellbare aber während dem Training konstante Millersche Zahl (siehe Dokumentation)
            self.MZ = int(config['Lernen']['mz'])

            # Einstellbare aber während dem Training konstante Zahl, ab wie vielen Fehlern eine Karte als schwierig gilt
            self.fehlertoleranz = int(config['Lernen']['ft'])
        except:
            self.MZ = 7
            self.fehlertoleranz = 2

        # Liste für die noch ungelerten Vokabeln
        self.ungelernt = []

        # Liste für die Vokabeln, welche gerade gelernt werden.
        self.lernend = [None for _ in range(self.MZ)]

        # Liste für die gelernten Vokabeln.
        self.gelernt = []

        # Die zulerneneden Wörter in die Listen verteilen.
        for karte in lernliste:
            if karte.lernfortschritt == 0:
                self.ungelernt.append(karte)
            elif karte.lernfortschritt == 1:
                # Auch bereits lernende Karten werden den Untelernten hinzugefügt
                self.ungelernt.append(karte)
            else:
                # Hier könnte man jetzt die anderen Karten hinzufügen, allerdings bring das eh nichts.
                # Im Gegenteil, sonst ist es nicht möglich, am Schluss einfach len(self.gelernt) zu nehmen
                # um herauszufinden, wie viele Vocis gelernt wurden.

                # Ist jetzt trotzdem gemacht für die Fortschrittsanzeige
                self.gelernt.append(karte)
                pass

        # Falls es nichts zu lernen gibt
        if len(self.ungelernt) == 0 and self.lernend == [None for i in range(self.MZ)]:
            raise TrainingFertig

        # self.debug_prints("Initialisierung des Controllers")

    def debug_prints(self, position: str = ""):
        """
        Eine kleine nützliche Methode, die einige Debug Prints ausgibt.
        """
        if position != "":
            rprint(f"[yellow] {position} ---------------------------")

        rprint(f"Cursor: {self.i}     (MZ = {self.MZ})")

        rprint("[blue]Ungelernt:")
        rprint(self.ungelernt)

        rprint("[blue]lernend:")
        rprint(self.lernend)

        rprint("[blue]gelernt:")
        rprint(self.gelernt)

    def fortschritt(self) -> list:
        """
        Gibt eine Tupel zurück, in der alle Daten enthalten sind, um den Fortschrittsbalken zu zeichnen.
        """
        anz_gesamt = len(self.ungelernt) + sum(1 for element in self.lernend if element is not None) + len(self.gelernt)
        fortschritts_daten = []

        # Zuerst im Hintergrund Gelb
        farbe_lernende = QColor(252, 186, 3)  # Gelb
        fortschritts_daten.append((farbe_lernende, 0, 1))

        # Grüner Balken für gelernte Wörter
        anteil_gelernte = len(self.gelernt) / anz_gesamt
        farbe_gelernte = QColor(197, 225, 196)  # Sanftes Grün
        eintrag_gelernte = (farbe_gelernte, 0, anteil_gelernte)
        fortschritts_daten.append(eintrag_gelernte)

        # Roter Balken für ungelernte Wörter
        anteil_ungelernte = len(self.ungelernt) / anz_gesamt
        farbe_ungelernte = QColor(225, 171, 171)  # Sanftes Rot
        eintrag_ungelernte = (farbe_ungelernte, 1 - anteil_ungelernte, 1)
        fortschritts_daten.append(eintrag_ungelernte)

        return fortschritts_daten

    def set_MZ(self, MZ: int) -> int:
        """
        Kleiner Setter um die Millersche Zahl zu ändern.
        Optimalerweise liegt MZ zwischen 5 und 9.
        :return Die vorherige MZ
        """
        alte_MZ = self.MZ
        self.MZ = MZ
        self.lernend = [None for i in range(self.MZ)]
        return alte_MZ

    def set_fehlerkonstante(self, fehlertoleranz: int) -> int:
        """
        Kleiner Setter um die Fehlertoleranz zu ändern.
        Die Fehlertoleranz bestimmt ab wie vielen falschen Antworten ein Karte als schwierig eingestuft wird.
        :return: Die vorherige Fehlerkonstante
        """
        alte_fehlerkonstante = self.fehlertoleranz
        self.fehlertoleranz = fehlertoleranz
        return alte_fehlerkonstante

    def frage(self) -> (Karte, bool):
        """
        Diese Funktion ruft das Trainingsfenster auf, um die Kartendaten für das nächste Wort zu bekommen.
        Es wird zuerst nachgeschaut, ob ein Voci an der aktuellen i-Position ist, wenn nicht wird eines nachgefüllt.
        Dann wird je nach Lernfortschritt das Wort gezeigt oder abgefragt.
        :return: Kartendaten, karte_zeigen: bool
        """
        # self.debug_prints("-------------------- FRAGE")
        nachgefuellt = False
        while not nachgefuellt:
            if self.lernend[self.i] is None:
                # Vokabular nachfüllen falls möglich.
                try:
                    self.lernend[self.i] = self.ungelernt.pop(0)
                    nachgefuellt = True

                except IndexError:
                    # Es gibt keine Ungelernten Wörter mehr, deshalb wird jetzt die Lernend Liste kleiner
                    self.lernend.pop(self.i)
                    self.MZ -= 1
                    if self.MZ == 0:
                        raise TrainingFertig

                    self.i = self.i % self.MZ
            else:
                nachgefuellt = True

        if self.lernend[self.i].lernfortschritt == 0:
            # Zeigen
            self.lernend[self.i].lernfortschritt = 1
            self.update_lernfortschritt(self.lernend[self.i].ID, 1)
            karte = self.lernend[self.i]
            self.i = (self.i + 1) % self.MZ
            return karte, True
        else:
            # Fragen
            return self.lernend[self.i], False

    def antwort(self, richtig_beantwortet: bool, neubewertung: bool = False) -> Karte:
        """
        Diese Funktion wird vom Fenster aufgerufen, um den Controller über das Resultat der letzten Abfrage
        zu informieren
        :param neubewertung: Ob eine neue Karte bewertet wird oder wieder die alte.
        :param richtig_beantwortet: Boolean, ob der Benutzer die Frage richtig beantwortet hatte.
        :return: Die Karte mit der aktualisierten Schwierigkeit
        """

        # if neubewertung:
        #     print("neubewertung", self.alte_karte)
        #     self.lernend[self.i] = copy.deepcopy(self.alte_karte)
        #     self.i = self.altes_i
        # else:
        #     self.lernend[self.i] = copy.deepcopy(self.neue_karte)
        #     self.alte_karte = copy.deepcopy(self.lernend[self.i])
        if neubewertung:
            self.stand_speicherung(wiederherstellung=True)
        else:
            self.stand_speicherung()

        # Erste abfrage eines Vocis -> nicht mehr unbekannt
        if self.lernend[self.i].schwierigkeit_max == -1:
            self.lernend[self.i].schwierigkeit_max = 0
            self.update_schwierigkeit_max(self.lernend[self.i].ID, 0)

        #
        if richtig_beantwortet:
            # Richtig beantwortet -> Einmal Fehlertoleranz von der Trainingsschwierigkeit abziehen
            self.lernend[self.i].schwierigkeit_training -= self.fehlertoleranz

            if self.lernend[self.i].schwierigkeit_training < 0:
                # Karte ist fertig gelernt
                self.lernend[self.i].lernfortschritt = 2
                self.update_lernfortschritt(self.lernend[self.i].ID, 2)

                # Der Liste der gelernten Karten hinzufügen
                self.gelernt.append(self.lernend[self.i])

                # Aktualisierte Karte speichern
                aktualisierte_karte = self.lernend[self.i]

                # Platz freigeben, damit später eine nachgeladen werden kann
                # noinspection PyTypeChecker
                self.lernend[self.i] = None

            else:
                # Aktualisierte Karte speichern
                aktualisierte_karte = self.lernend[self.i]

        else:
            # Frage wurde Falsch beantwortet
            # Trainingsschwierigkeit erhöhen
            self.lernend[self.i].schwierigkeit_training += 1

            # Jetzt wird nur noch ermittelt, ob die Schwierigkeit der Karte einen neuen Peak hat, weil dann muss
            # die Schwierigkeit Max aktualisiert werden.
            aktuelle_schwierigkeit_max = self.lernend[self.i].schwierigkeit_training // self.fehlertoleranz
            if self.lernend[self.i].schwierigkeit_max < aktuelle_schwierigkeit_max <= 3:
                # Update
                self.lernend[self.i].schwierigkeit_max = aktuelle_schwierigkeit_max
                self.update_schwierigkeit_max(self.lernend[self.i].ID, aktuelle_schwierigkeit_max)

            # Aktualisierte Karte speichern
            aktualisierte_karte = self.lernend[self.i]

        self.i = (self.i + 1) % self.MZ

        # self.debug_prints("----------------------- Antwort")

        return aktualisierte_karte

    def stand_speicherung(self, wiederherstellung: bool = False):
        """
        Speichert oder stellt den gespeicherten Lernstand wieder her.
        """
        if not wiederherstellung:
            # Speichern
            self.gespeichert_ungelernt = copy.deepcopy(self.ungelernt)
            self.gespeichert_lernend = copy.deepcopy(self.lernend)
            self.gespeichert_gelernt = copy.deepcopy(self.gelernt)
            self.gespeichert_i = self.i
            self.gespeichert_aenderungen = []
        else:
            # Wiederherstellen
            self.ungelernt = copy.deepcopy(self.gespeichert_ungelernt)
            self.lernend = copy.deepcopy(self.gespeichert_lernend)
            self.gelernt = copy.deepcopy(self.gespeichert_gelernt)
            self.i = self.gespeichert_i

            # Änderungen rückgängig machen
            for aenderung in self.gespeichert_aenderungen:
                if aenderung[0] == "lernfortschritt":
                    self.update_lernfortschritt(aenderung[1], aenderung[2], registrieren=False)
                elif aenderung[0] == "schwierigkeit":
                    self.update_schwierigkeit_max(aenderung[1], aenderung[2], registrieren=False)
            self.gespeichert_aenderungen = []

    def update_lernfortschritt(self, karte_id: int, neuer_lernfortschritt: int, registrieren: bool = True):
        """Kleine Funktion um auch in der Datenbank die Werte upzudaten."""
        if self.training_speichern:
            cursor = self.DBCONN.cursor()
            if registrieren:
                # Alterlernfortschritt herausfinden
                sql = "SELECT lernfortschritt FROM main.karte WHERE karte_id=?"
                cursor.execute(sql, (karte_id,))
                alter_lernfortschritt = cursor.fetchone()[0]
                self.gespeichert_aenderungen.append(["lernfortschritt", karte_id, alter_lernfortschritt])

            sql = """
            UPDATE karte SET lernfortschritt=? WHERE karte_id=?"""
            cursor.execute(sql, (neuer_lernfortschritt, karte_id))
            cursor.close()
            self.DBCONN.commit()

    def update_schwierigkeit_max(self, karte_id: int, neue_schwierigkeit: int, registrieren: bool = True):
        """Kleine Funktion um auch in der Datenbank die Werte upzudaten."""
        if self.training_speichern:
            cursor = self.DBCONN.cursor()

            if registrieren:
                # Alterlernfortschritt herausfinden
                sql = "SELECT schwierigkeit FROM main.karte WHERE karte_id=?"
                cursor.execute(sql, (karte_id,))
                alte_schwierigkeit = cursor.fetchone()[0]
                self.gespeichert_aenderungen.append(["schwierigkeit", karte_id, alte_schwierigkeit])

            sql = """
            UPDATE karte SET schwierigkeit=? WHERE karte_id=?"""
            cursor.execute(sql, (neue_schwierigkeit, karte_id))
            cursor.close()
            self.DBCONN.commit()


class TrainingFertig(Exception):
    """
    Das ist eine eigene Exception, die geworfen wird, wenn eine weitere Karte geladen wird,
    obwohl das Training fertig ist.
    """
    def __init__(self):
        super().__init__()
