# -*- coding: utf-8 -*-
"""
network.py
Enthält die Klassen Netzwerk. Siehe deren Doc-String
"""

import pickle
import socket


class Network:
    """
    Die Netzwerkklasse stellt die Verbindung zum Server her und
    stellt Funktionen für alle Aufgaben, die den Server betreffen (Hoch-, Herunterladen, Profil ...) bereit.
    Die wichtigste Funktion ist sendRecv. Die anderen stellen vorallem eine Zwischenstufe dar, damit man sich nicht
    mitten im Programm mit KIDs und der Ordnung der Argumente beschäftigen muss.
    """
    def __init__(self, ADDR=("vocitrainer.admuel.ch", 4647)):
        self.ADDR = ADDR
        self.HEADER = 128
        self.FORMAT = 'utf-8'
        self.CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CONN.connect(ADDR)

    def sendRecv(self, liste: list):
        """
        Eine Funktion, welche eine Anfrage an den Server senden und dessen Antwort zurückgibt.
        """

        liste = pickle.dumps(liste)
        msg_length = len(liste)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.CONN.send(send_length)
        self.CONN.send(liste)

        response_length = self.CONN.recv(self.HEADER)
        # print("Response_Length String: ", response_length)
        response_length = response_length.decode(self.FORMAT)

        komplett = False
        ganze_nachricht = b''
        while not komplett:
            ganze_nachricht += self.CONN.recv(int(response_length) - len(ganze_nachricht))
            # print("Response Length: ", response_length, " Tatsächliche angekommen: ", len(ganze_nachricht))
            if len(ganze_nachricht) == int(response_length):
                komplett = True

        response = pickle.loads(ganze_nachricht)
        return response

    def vociset_suche(self, prompt: str, anzahl_resultate: int, sprache: str = "Alle") -> list:
        """
        Diese Funktion fordert den Server auf, nach dem Suchprompt zu suchen und die Ergebnisse zu senden
        :param prompt: Der Suchprompts
        :param anzahl_resultate: Die Anzahl Resultate, die der Server fetchen soll
        :param sprache: Hier kann ein Filter für die Sprache eingestellt werden
        :return: Die Ergebnisse der Suche
        """
        nachricht = [3, prompt, anzahl_resultate, sprache]
        antwort = self.sendRecv(nachricht)

        return antwort[1]

    def vociset_herunterladen(self, set_id: int) -> tuple:
        """
        Lädt das Vociset und die dazugehörigen Karten vom Server herunter
        :param set_id: set_id des Vocisets
        :return: Ein Tupel,
            Das erste Element enthält den Vociset Datensatz,
            Das zweite Element eine Liste von Karten Datensätzen

            v.set_id, v.set_name, v.beschreibung, v.sprache, v.anz_downloads, u.benutzername, u.gesperrt
        """
        nachricht = [4, set_id]
        antwort = self.sendRecv(nachricht)

        return antwort[1], antwort[2]

    def user_einloggen(self, email: str, passwort: bytes) -> bool:
        """
        Versucht einen Benutzer mit den Logindaten einzuloggen
        :param email: Die E-Mail des Benutzers
        :param passwort: Das bereits gehashte Passwort des Benutzers
        :return: Erfolg des einloggens (bool)
        """
        nachricht = [5, email, passwort]
        try:
            antwort = self.sendRecv(nachricht)
        except:
            return False

        return antwort[1]

    def user_registrieren(self, benutzername: str, email: str, passwort: bytes) -> int:
        """
        Fordert Registierung eines neuen Benutzers auf dem Server an.
        :param benutzername: Ein vom Benutzergewählter, öffentlich sichtbarer Nickname
        :param email: Die E-Mail des zu registrierenden Benutzers (Bereits auf Möglichkeit überprüft)
        :param passwort: Das bereits gehashte Passwort
        :return: interger
            0 = Erfolg
            1 = Benutzername bereits gewählt
            2 = E-Mail bereits registriert
            3 = Fehler beim Versenden der E-Mail mit dem Verifikationscode
        """
        nachricht = [6, benutzername, email, passwort]
        antwort = self.sendRecv(nachricht)

        return antwort[1]

    def registierung_abschliessen(self, bestaetigungscode: int):
        """
        Die Registierung wird erst abgeschlossen, wenn der Server den korrekten Verifikationscode erhält.
        :param bestaetigungscode: Der Code, den der Benutzer bekommen hat bzw. eingegeben hat.
        :return: Erfolg bool
        """
        nachricht = [7, bestaetigungscode]
        antwort = self.sendRecv(nachricht)

        return antwort[1]

    def vociset_hochladen(self, vociset_datensatz, karten_datensaetze):
        """
        Lädt das Set auf den Server hoch.
        :param vociset_datensatz: Der Datensatz des Sets
        :param karten_datensaetze: Die Daten der einzelnen Karten (2D-Liste)
        :return: bool Erfolg
        """
        nachricht = [8, vociset_datensatz, karten_datensaetze]

        try:
            antwort = self.sendRecv(nachricht)
            return antwort[1]

        except:
            return False

    def verwalten_info(self):
        """
        Fordert Informationen aller vom momentan angemeldeten User hochgeladenen Vocisets an.
        :return: False bei Fehler, sonst die Liste der vociset-Datensätze
        Vociset_Datensatz = [set_id, set_name, beschreibung, sprache, anz_downloads]
        """
        nachricht = [9]
        try:
            antwort = self.sendRecv(nachricht)
            return antwort[1]
        except:
            return False

    def verwalten_aktion(self, set_id: int, aktion: int) -> bool:
        """
        Führt mit einem der Sets (falls es dem angemeldeten User gehört) eine Aktion auf dem Server aus (löschen)
        :param set_id: Das Set mit dem etwas gemacht werden sollte (muss dem angemeldeten User gehören)
        :param aktion: 0 = Löschen
        :return: bool Erfolg
        """
        nachricht = [10, set_id, aktion]

        antwort = self.sendRecv(nachricht)
        return antwort[1]

    def konto_loeschen(self):
        """
        Fordert den Server auf das Konto des momentan angemeldeten Users zu löschen
        :return: bool Erfolg
        """
        nachricht = [11]

        antwort = self.sendRecv(nachricht)
        return antwort[1]


if __name__ == "__main__":
    net = Network(("localhost", 4647))

    # Beim direkten ausführen einen Test laufen lassen
    print(net.sendRecv([1, "Hallo"]))
