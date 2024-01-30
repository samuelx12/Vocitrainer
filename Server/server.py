# -*- coding: utf-8 -*-
"""
server.py
Hier ist die Hauptdatei des Servers.
"""

import socket
import ssl
from rich import traceback
from rich import print as rprint
from session import Session

# Server Version
VERSION = "v0.1.0"

# Für Debugzwecke: Schönes Traceback installieren
traceback.install()

PORT = 4647
SERVER = "localhost"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server = ssl.wrap_socket(
#     sock=server,
#     keyfile="server.key",
#     certfile="server.crt",
#     server_side=True,
#     cert_reqs=ssl.CERT_NONE,
#     ssl_version=ssl.PROTOCOL_SSLv23
# )

# Gebe Informationen aus:
rprint("[magenta]#############################")
rprint(f"[blue]Server-Version: [cyan]{VERSION}")
rprint("[blue]Starte Vocitrainer-Server...")
rprint(f"[blue]Adress: {SERVER}")
rprint(f"[blue]Port: {PORT}")

try:
    server.bind(ADDR)
    server.listen(5)  # Server aktivieren, die Zahl ist die Anzahl maximaler Verbindungen
except Exception as e:
    rprint("[red]Start fehlgeschlagen!")
    rprint("[magenta]#############################")

    print()
    rprint("[red]Fehlermeldung:")
    rprint(f"[yellow]{str(e)}")

    exit(1)

rprint(f"[green]Erfolgreich gestartet!")
rprint("[magenta]#############################")
print()

# Ab jetzt werden in einer Endlosschleife neue Verbindungen angenommen
# und Sessions für jeden neuen Client erstellt und gestartet
while True:
    rprint("[cyan]Warte auf neue Verbindungen...")
    conn, addr = server.accept()
    session = Session(conn, addr)
    rprint("[green]Starte neue Session!")
    session.start()
