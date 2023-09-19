# -*- coding: utf-8 -*-
"""
server.py
Beschreibung
"""

import socket
import ssl
from rich import traceback
from session import Session

# Für Debugzwecke: Schönes Traceback installieren
traceback.install()

PORT = 4647
SERVER = "localhost"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Vor wrap")
# server = ssl.wrap_socket(
#     sock=server,
#     keyfile="server.key",
#     certfile="server.crt",
#     server_side=True,
#     cert_reqs=ssl.CERT_NONE,
#     ssl_version=ssl.PROTOCOL_SSLv23
# )
print("nach wrap")
server.bind(ADDR)
server.listen(5)  # Server aktivieren, die Zahl ist die Anzahl maximaler Verbindungen


# Ab jetzt werden in einer Endlosschleife neue Verbindungen angenommen
# und Sessions für jeden neuen Client erstellt und gestartet
while True:
    print("Warte auf neue Verbindungen...")
    conn, addr = server.accept()
    session = Session(conn, addr)
    print("Starte neue Session!")
    session.start()
