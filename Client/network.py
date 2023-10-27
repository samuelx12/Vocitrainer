# -*- coding: utf-8 -*-
"""
network.py
Hier sind verschiedene Helfer die die Kommunikation mit dem Server betreffen.
"""

import pickle
import socket
import ssl
from typing import Iterable


class Network:
    """
    Die Netzwerkklasse stellt die Verbindung zum Server her und
    stellt Funktionen für alle Aufgaben, die den Server betreffen (Hoch-, Herunterladen, Profil ...) bereit.
    Die wichtigste Funktion ist sendRecv. Die anderen stellen vorallem eine Zwischenstufe dar, damit man sich nicht
    mitten im Programm mit KIDs und der Ordnung der Argumente beschäftigen muss.
    """
    def __init__(self, ADDR=("localhost", 4647)):
        self.ADDR = ADDR
        self.HEADER = 128
        self.FORMAT = 'utf-8'
        self.CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.CONN = ssl.wrap_socket(
        #     sock=self.CONN,
        #     keyfile=None,
        #     certfile=None,
        #     server_side=False,
        #     cert_reqs=ssl.CERT_NONE,
        #     ssl_version=ssl.PROTOCOL_SSLv23
        # )
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

        response_length = self.CONN.recv(self.HEADER).decode(self.FORMAT)
        response = self.CONN.recv(int(response_length))
        response = pickle.loads(response)
        return response

    def vociset_suche(self, prompt: str, anzahl_resultate: int) -> list:
        """
        Diese Funktion fordert den Server auf, nach dem Suchprompt zu suchen und die Ergebnisse zu senden
        :param prompt: Der Suchprompt
        :param anzahl_resultate: Die Anzahl Resultate, die der Server fetchen soll
        :return: Die Ergebnisse der Suche
        """
        nachricht = [3, prompt, anzahl_resultate]
        antwort = self.sendRecv(nachricht)
        print("Ergebnisse der Suche: ", antwort[1])
        return antwort[1]

    def vociset_herunterladen(self, set_id: int) -> tuple:
        """
        Lädt das Vociset und die dazugehörigen Karten vom Server herunter
        :param set_id: set_id des Vocisets
        :return: Ein Tupel,
            Das erste Element enthält den Vociset Datensatz,
            Das zweite Element eine Liste von Karten Datensätzen
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
        antwort = self.sendRecv(nachricht)

        return antwort[1]

    def user_registrieren(self, benutzername: str, email: str, passwort: bytes) -> int:
        """
        Registriert einen neuen Benutzer beim Server
        :param benutzername: Ein vom Benutzergewählter, öffentlich sichtbarer Nickname
        :param email: Die E-Mail des zu registrierenden Benutzers (Bereits auf Möglichkeit überprüft)
        :param passwort: Das bereits gehashte Passwort
        :return: interger
            0 = Erfolg
            1 = Benutzername bereits gewählt
            2 = E-Mail bereits registriert
        """
        nachricht = [6, benutzername, email, passwort]
        antwort = self.sendRecv(nachricht)

        return antwort[1]


if __name__ == "__main__":
    net = Network(("localhost", 4647))

    print(net.sendRecv([1, "Hallo"]))
