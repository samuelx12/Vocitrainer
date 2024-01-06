# -*- coding: utf-8 -*-
"""
trainingscontroller.py
Hierhin kommen die Kontroll-Klassen für das Training
"""

from karte_tuple import Karte


class TestTraining:
    def __int__(self):
        pass

    def frage(self):
        return ([1, "Haus", "house", "Ein Gebäude", 75, False, 3],)

    def antwort(self, antwort):
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


class TC_Intelligent:
    """
    Hier steht der Controller für den Intelligenten Lernmodus.
    Über die Algorithmik und die psychologischen Hintergrundgedanken steht genaueres
    in eigenen Dateien im "Dokumentation"-Ordner.

    karte = [
        [kartendaten],
        schwierigkeit: int,
        gezeigt: bool
    ]
    """
    def __init__(self):
        # Countervariable
        self.i = 0

        # Einstellbare aber während Training konstante Millersche Zahl (siehe Dokumentation)
        self.MZ = 5

        # Liste für die noch ungelerten Vokabeln
        self.ungelernt = []

        # Liste für die Vokabeln, welche gerade gelernt werden.
        self.lernend = []

        # Liste für die gelernten Vokabeln.
        self.gelernt = []



    def frage(self):
        pass

    def antwort(self, antowrt: str):
        pass


class TrainingFertig(Exception):
    """
    Das ist eine eigene Exception, die geworfen wird, wenn eine weitere Karte geladen wird,
    obwohl das Training fertig ist.
    """
    def __init__(self):
        super().__init__()
