# -*- coding: utf-8 -*-
"""
trainingscontroller.py
Hierhin kommen die Kontroll-Klassen für das Training
"""

from karte_tuple import Karte
from typing import Iterable
from rich import print as rprint
from sqlite3 import Connection


class TestTraining:
    def __int__(self):
        pass

    @staticmethod
    def frage():
        return ([1, "Haus", "house", "Ein Gebäude", 75, False, 3],)

    @staticmethod
    def antwort(antwort):
        resultat = antwort == "house"
        return [1, "Haus", "house", "Ein Gebäude", 75, False, 3], resultat


class TC_Einfach:
    """
    Ein einfacher Trainingscontroller, der Wörter immer wiederholt, bis alle einmal richtig geschrieben wurden.
    """
    def __init__(self, lernliste):
        self.lernliste = lernliste
        self.i = 0  # Counter

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

        return neues_wort, False

    def antwort(self, resultat: bool):
        """
        Mit dieser Funktion wird der Trainingscontroller informiert, ob die Frage richtig beantwortet wurde
        """

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

    Fehlertolerenz
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

        # Einstellbare aber während dem Training konstante Millersche Zahl (siehe Dokumentation)
        self.MZ = 5

        # Einstellbare aber während dem Training konstante Zahl, ab wie vielen Fehlern eine Karte als schwierig gilt.
        self.fehlertoleranz = 2

        # Liste für die noch ungelerten Vokabeln
        self.ungelernt = []

        # Liste für die Vokabeln, welche gerade gelernt werden.
        self.lernend = [None for i in range(7)]

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
                pass

        self.debug_prints("Initialisierung des Controllers")

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
        self.debug_prints("-------------------- FRAGE")
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

    def antwort(self, richtig_beantwortet: str) -> Karte:
        """
        Diese Funktion wird vom Fenster aufgerufen, um den Controller über das Resultat der letzten Abfrage
        zu informieren
        :param richtig_beantwortet: Boolean, ob der Benutzer die Frage richtig beantwortet hatte.
        :return: Die Karte mit der aktualisierten Schwierigkeit
        """
        self.debug_prints("----------------------- Antwort")
        if richtig_beantwortet:
            if self.lernend[self.i].schwierigkeit_max == -1:
                # Voci wurde zum erstenmal abgefragt und war gleich richtig
                self.lernend[self.i].schwierigkeit_max = 0

                self.update_schwierigkeit_max(self.lernend[self.i].ID, 0)

                # Karte für die Anzeige nachher speichern
                aktualisierte_karte = self.lernend[self.i]

            elif self.lernend[self.i].schwierigkeit_training >= self.fehlertoleranz:
                # Die Karte war zuvor mehrmals falsch, sie wird jetzt doch für
                # die Trainingszeitdauer als einfacher eingestuft.
                self.lernend[self.i].schwierigkeit_training = (
                        self.lernend[self.i].schwierigkeit_training - self.fehlertoleranz)

                # Aktualisierte Karte speichern
                aktualisierte_karte = self.lernend[self.i]

            else:
                # Karte ist fertig gelernt
                self.lernend[self.i].schwierigkeit_training = 0
                self.lernend[self.i].lernfortschritt = 2
                self.gelernt.append(self.lernend[self.i])
                self.update_lernfortschritt(self.lernend[self.i].ID, 2)

                # Aktualisierte Karte speichern
                aktualisierte_karte = self.lernend[self.i]

                # noinspection PyTypeChecker
                self.lernend[self.i] = None

        else:
            # Frage wurde Falsch beantwortet
            # Trainingsschwierigkeit erhöhen
            self.lernend[self.i].schwierigkeit_training=self.lernend[self.i].schwierigkeit_training + 1

            # Jetzt wird nur noch ermittelt, ob die Schwierigkeit der Karte einen neuen Peak hat, weil dann muss
            # die Schwierigkeit Max aktualisiert werden.
            if self.lernend[self.i].schwierigkeit_training > self.lernend[self.i].schwierigkeit_max:

                neue_schwierigkeit_max = self.lernend[self.i].schwierigkeit_training // self.fehlertoleranz

                self.lernend[self.i].schwierigkeit_max=neue_schwierigkeit_max

                self.update_schwierigkeit_max(self.lernend[self.i].ID, neue_schwierigkeit_max)

            # Aktualisierte Karte speichern
            aktualisierte_karte = self.lernend[self.i]

        self.i = (self.i + 1) % self.MZ

        return aktualisierte_karte

    def update_lernfortschritt(self, karte_id: int, neuer_lernfortschritt: int):
        """Kleine Funktion um auch in der Datenbank die Werte upzudaten."""
        if self.training_speichern:
            cursor = self.DBCONN.cursor()
            sql = """
            UPDATE karte SET lernfortschritt=? WHERE karte_id=?"""
            cursor.execute(sql, (neuer_lernfortschritt, karte_id))
            cursor.close()
            self.DBCONN.commit()

    def update_schwierigkeit_max(self, karte_id: int, neue_schwierigkeit: int):
        """Kleine Funktion um auch in der Datenbank die Werte upzudaten."""
        if self.training_speichern:
            cursor = self.DBCONN.cursor()
            sql = """
            UPDATE karte SET lernfortschritt=? WHERE karte_id=?"""
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
