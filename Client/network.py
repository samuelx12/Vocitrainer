# -*- coding: utf-8 -*-
"""
network.py
Hier sind verschiedene Helfer die die Kommunikation mit dem Server betreffen.
"""

import pickle
import socket
import ssl


class Network:
    def __init__(self, ADDR):
        self.ADDR = ADDR
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CONN = ssl.wrap_socket(
            sock=self.CONN,
            keyfile=None,
            certfile=None,
            server_side=False,
            cert_reqs=ssl.CERT_NONE,
            ssl_version=ssl.PROTOCOL_SSLv23
        )
        self.CONN.connect(ADDR)

    def sendRecv(self, liste):
        """
        Funktion die eine Anfrage an den Server senden und dessen Antwort zurückgibt.
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


if __name__ == "__main__":
    net = Network(("localhost", 4647))

    print(net.sendRecv([1, "Hallo"]))
