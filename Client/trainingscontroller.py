"""
trainingscontroller.py
Hierhin kommen die Kontroll-Klassen für das Training
"""


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
    def __init__(self):
        self.lernliste = [
            [1, "Haus", "house", "Ein Gebäude", 75, False, 3],
            [2, "Hund", "dog", "Haustier", 25, True, 3],
            [3, "Kuh", "cow", "Tier, das Milch gibt", 50, False, 3]
        ]
        self.i = 0  # Counter

    def frage(self):
        return self.lernliste[self.i],

    def antwort(self, antwort):
        print("Wort Nummer: ", self.i)
        resultat = antwort == self.lernliste[self.i][2]
        return_info = self.lernliste[self.i], resultat

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

        return return_info
