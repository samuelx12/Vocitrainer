# -*- coding: utf-8 -*-
"""
session.py
Hier ist der Thread für die Session des Servers mit dem Client
"""

import threading
import ssl


class Session(threading.Thread):
    """
    Damit mehrere Clients gleichzeitig vom Server verarbeitet werden können, werden Clients in Threads behandelt.
    Dies ist dieser Session Thread.
    """
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def run(self) -> None:
        # Zuerst Verbindung verschlüsseln
        self.conn = ssl.wrap_socket(
            sock=self.conn,
            keyfile=None,
            certfile=None,
            server_side=True,
            cert_reqs=ssl.CERT_NONE,
            ssl_version=ssl.PROTOCOL_SSLv23
        )
