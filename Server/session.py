# -*- coding: utf-8 -*-
"""
session.py
Hier ist der Thread für die Session des Servers mit dem Client
"""

import threading
import ssl
import pickle
from typing import List, Iterable


class Session(threading.Thread):
    """
    Damit mehrere Clients gleichzeitig vom Server verarbeitet werden können, werden Clients in Threads behandelt.
    Dies ist dieser Session Thread.
    """
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

        # Konstanten
        self.HEADER = 64
        self.FORMAT = 'utf-8'

    def empfangen(self) -> Iterable:
        """
        Funktion für das Empfangen von Nachrichten vom Server. Gibt die fertig entpickelte Liste zurück
        """
        # Erste Nachricht empfangen, welche die Grösse der zweiten Nachricht enthaltet
        msg_length = self.conn.recv(self.HEADER).decode(self.FORMAT)
        msg_length = int(msg_length)

        # Zweite Nachricht empfangen
        msg = self.conn.recv(msg_length)
        msg = pickle.loads(msg)

        return msg

    def senden(self, msg) -> None:
        # Funktion die eine gepickelte Liste an server_conn sendet

        # Nachricht pickeln
        msg = pickle.dumps(msg)

        # Länge der Nachricht ermitteln und zuerst diese senden
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.conn.send(send_length)

        # Nachricht selbst senden
        self.conn.send(msg)

        return

    def run(self) -> None:
        # Zuerst Verbindung verschlüsseln

        print(self.empfangen())

        self.senden([3, "Auch Hallo"])
