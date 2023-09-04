# -*- coding: utf-8 -*-
"""
server.py
Beschreibung
"""

import socket
from rich import traceback
from session import Session

# Für Debugzwecke: Schönes Traceback installieren
traceback.install()

PORT = 4647
SERVER = "localhost"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(5)  # Server aktivieren, die Zahl ist die Anzahl maximaler Verbindungen


# Ab jetzt werden in einer Endlosschleife neue Verbindungen angenommen
# und Sessions für jeden neuen Client erstellt und gestartet
while True:
    conn, addr = server.accept()
    session = Session(conn, addr)
    session.start()
