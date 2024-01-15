# -*- coding: utf-8 -*-
"""
session.py
Hier ist der Thread für die Session des Servers mit dem Client
"""

import threading
import ssl
import pickle
import time
from typing import List, Iterable
from datetime import datetime
import sqlite3


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
        self.HEADER = 128
        self.FORMAT = 'utf-8'
        self.SALT = b'\xcd\xae\xd1C\xc0#a\x8ch\x83\x95\xc5%l\xc7\x14'

        self.eingeloggter_user_id = None
        self.verbunden = True

    def empfangen(self) -> list:
        """
        Funktion für das Empfangen von Nachrichten vom Server. Gibt die fertig entpickelte Liste zurück
        """
        # Erste Nachricht empfangen, welche die Grösse der zweiten Nachricht enthaltet
        msg_length = self.conn.recv(self.HEADER)

        if msg_length == b'':
            # Client hat die Verbindung geschlossen
            self.CURSOR.close()
            self.DBCONN.close()
            self.verbunden = False
            return [1]

        msg_length = msg_length.decode(self.FORMAT)
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
        """
        Run
        :return: None
        """

        # Zuerst Verbindung verschlüsseln (momentan entfernt)

        # print(self.empfangen())
        #
        # self.senden([3, "Auch Hallo"])

        print("DBconn erstellt")
        self.DBCONN = sqlite3.connect('serverdb.db')
        self.CURSOR = self.DBCONN.cursor()

        while self.verbunden:
            nachricht = self.empfangen()
            kid = nachricht[0]
            antwort = []

            if kid == 1:
                # Verbindung wird beendet
                print("Verbindung wurde geschlossen")
                pass
            elif kid == 2:
                # Authentifizierung
                pass
            elif kid == 3:
                """
                Set suche:
                [kid, prompt, sprache]
                """

                antwort = self.beantworte_kid3(nachricht)

            elif kid == 4:
                """
                Set Herunterladen
                [kid, [Set Datensatz], [Liste der [Karten Datensätze]]]
                """

                antwort = self.beantworte_kid4(nachricht)

            elif kid == 5:
                """
                Login
                """

                antwort = self.beantworte_kid5(nachricht)

            elif kid == 6:
                """
                Registrieren
                """

                antwort = self.beantworte_kid6(nachricht)

            elif kid == 7:
                """
                E-Mail-Überprüfung
                """

                antwort = self.beantworte_kid7(nachricht)

            elif kid == 8:
                """
                Set auf den Server hochladen
                """

                antwort = self.beantworte_kid8(nachricht)

            elif kid == 9:
                """
                Verwalten Informationen angefordert
                """

                antwort = self.beantworte_kid9(nachricht)

            elif kid == 10:
                """
                Verwalten: Eine Aktion (löschen) wird gefordert
                """

                antwort = self.beantworte_kid10(nachricht)

            else:
                antwort = ["FEHLER"]
                print("ERROR mit kid:")
                print(kid)

            if self.verbunden:
                self.senden(antwort)

    def beantworte_kid3(self, nachricht) -> list:
        """
        Set suche:
        [kid, prompt, anzahl_resultat, sprache]
        """

        def zaehle_treffer(title: str) -> int:
            """
            Zählt die Anzahl Wörter im Titel, die im Suchbegriff vorkommen.
            :param title: Der Titel in dem gesucht werden soll
            :return: Die Anzahl der Wörter im Titel, die im Suchbegriff vorkommen.
            """
            anz_treffer = sum(wort.lower() in title.lower() for wort in gesplitteter_prompt)
            return anz_treffer

        def trace_callback(statement):
            print("Ausgeführter SQL-Befehl:", statement)

        prompt: str = nachricht[1]
        anzahl_resultate: int = nachricht[2]
        sprache: str = nachricht[3]
        gesplitteter_prompt = prompt.split()

        # Ausgeführte Befehle für Debug Printen
        self.DBCONN.set_trace_callback(trace_callback)

        # Suchquery erstellen
        # Die 'LIKE's suchen alle sets heraus, welche eines der Wörter des Suchprompts im Namen haben
        query = """
            SELECT v.set_id, v.set_name, v.beschreibung, v.sprache, v.anz_downloads, u.benutzername, u.gesperrt
            FROM vociset v
            JOIN user u ON v.user_id = u.user_id
            WHERE (set_name LIKE '%' || ? || '%' OR beschreibung LIKE '%' || ? || '%'
"""
        for i in range(len(gesplitteter_prompt) - 1):
            query += " OR set_name LIKE '%'+?+'%' OR beschreibung LIKE '%'+?+'%'"

        query += ")"

        # Filterung nach Sprache
        if sprache != "Alle":
            query += f" AND sprache='{sprache}'"

        gesplitteter_prompt_doppelt = []
        for splitter in gesplitteter_prompt:
            gesplitteter_prompt_doppelt.append(splitter)
            gesplitteter_prompt_doppelt.append(splitter)

        self.CURSOR.execute(query, gesplitteter_prompt_doppelt)
        ergebnisse = self.CURSOR.fetchmany(anzahl_resultate)

        # Entfernung von gesperrten Usern
        i = 0
        for ergbnis in ergebnisse:
            if ergbnis[6] == 1:
                ergebnisse.pop(i)
            else:
                i += 1

        # Jetzt werden die Resultate danach geordnet, wie viele Wörter des Suchprompts darin enthalten sind.
        ergebnisse.sort(key=lambda resultat: zaehle_treffer((resultat[1] + resultat[2] + resultat[3])), reverse=True)

        return [3, ergebnisse]

    def beantworte_kid4(self, nachricht) -> list:
        """
        Set Herunterladen
        [kid, [Set Datensatz], [Liste der [Karten Datensätze]]]
        """
        set_id = nachricht[1]

        # SQL-Query um die Daten des gewünschten Vocisets zu kriegen
        query = """SELECT set_id, set_name, beschreibung, sprache FROM vociset WHERE set_id = ?"""
        self.CURSOR.execute(query, (set_id,))
        vociset_datensatz = self.CURSOR.fetchone()

        # SQL-Query um die Karten Datensätze zu erhalten
        query = """SELECT karte_id, wort, fremdwort, definition, bemerkung, set_id FROM karte WHERE set_id = ?"""
        self.CURSOR.execute(query, (set_id,))
        karten_datensaetze = self.CURSOR.fetchall()

        # Downloadzahl erhöhen
        query = """UPDATE vociset SET anz_downloads = anz_downloads + 1 WHERE set_id = ?;"""
        self.CURSOR.execute(query, (set_id,))
        self.DBCONN.commit()

        return [4, vociset_datensatz, karten_datensaetze]

    def beantworte_kid5(self, nachricht: list) -> List:
        """
        Login
        :param nachricht: [kid, email, passwort]
        :return: [kid, erfolg: bool]
        """
        # Kleine Verzögerung zur Sicherheit
        time.sleep(0.2)

        email = nachricht[1]
        passwort = str(nachricht[2])

        print("E-Mail>>", email)
        print("Login Passwort (hash): ", passwort)

        query = """SELECT user_id FROM user WHERE email = ? AND passwort = ?"""
        self.CURSOR.execute(query, (email, passwort))

        id = self.CURSOR.fetchone()
        print("ID: ", id)
        if id:
            self.eingeloggter_user_id = id[0]
            return [5, True]
        else:
            return [5, False]

    def beantworte_kid6(self, nachricht: list) -> list:
        """
        Registrieren
        :param nachricht: [kid, benutzername, email, passwort]
        :return: [kid, ergebnis: int]
        ergebnis:
            0 = Erfolg
            1 = Benutzername bereits gewählt
            2 = E-Mail bereits registriert
        """
        benutzername = nachricht[1]
        email = nachricht[2]
        passwort = str(nachricht[3])

        print("E-Mail>>", email)
        print("Registriertes Passwort (hash): ", passwort)

        # Überprüfen ob der Benutzername bereits existiert
        self.CURSOR.execute('SELECT COUNT(*) FROM user WHERE benutzername = ?', (benutzername,))
        resultat = self.CURSOR.fetchone()
        if resultat[0] > 0:
            return [6, 1]

        # Überprüfen ob die E-Mail schon registriert ist
        self.CURSOR.execute('SELECT COUNT(*) FROM user WHERE email = ?', (email,))
        resultat = self.CURSOR.fetchone()
        if resultat[0] > 0:
            return [6, 2]

        # Benutzer registrieren
        self.CURSOR.execute(
            f"INSERT INTO user (email, passwort, benutzername, gesperrt, erstellung) VALUES (?, ?, ?, 0, ?)",
            [email, passwort, benutzername, datetime.now()]
        )

        # Benutzer einloggen
        self.eingeloggter_user_id = self.CURSOR.lastrowid

        # Änderngen speichern
        self.DBCONN.commit()

        # Erfolg zurückmelden
        return [6, 0]

    def beantworte_kid7(self, nachricht: list) -> list:
        """
        E-Mail Überprüfung
        :param nachricht: [kid, code]
        :return: [kid, bool: erfolg]

        Das hier wäre eine Mögliche Erweiterung um dem ganzen eine Überprüfung von Emails hinzuzufügen.
        Allerdings wäre das viel Arbeit mit wenig Wirkung und steht nicht im Fokus meiner Arbeit.
        """
        pass

    def beantworte_kid8(self, nachricht: list) -> list:
        """
        Set auf den Server hochladen
        :param nachricht: [kid, [Set Datensatz], [Liste der [Karten Datensätze]]]
        :return: [kid, Erfolg]
        """

        try:
            vociset_datensatz = nachricht[1]
            karten_datensaetze = nachricht[2]

            # Query um den Vocisetzt-Datensatz einzufügen
            query = """
            INSERT INTO vociset (set_name, beschreibung, sprache, anz_downloads, user_id) VALUES (?, ?, ?, 0, ?)
            """

            self.CURSOR.execute(
                query,
                (vociset_datensatz[0], vociset_datensatz[1], vociset_datensatz[2], self.eingeloggter_user_id)
            )
            hochgeladenes_set_id = self.CURSOR.lastrowid

            # Schleife um die Karten einzufügen
            query = f"""
            INSERT INTO karte (wort, fremdwort, definition, bemerkung, set_id)
            VALUES (?, ?, ?, ?, {hochgeladenes_set_id})
            """
            for i in range(len(karten_datensaetze)):
                self.CURSOR.execute(
                    query,
                    (
                        karten_datensaetze[i][0],
                        karten_datensaetze[i][1],
                        karten_datensaetze[i][2],
                        karten_datensaetze[i][3]
                    )
                )

            self.DBCONN.commit()

            return [8, True]

        except Exception as e:
            # Fehlermeldung zurückschicken
            return [8, False]

    def beantworte_kid9(self, nachricht: list) -> list:
        """
        Client fordert Informationen zu seinen hochgeladenen Vocisets an
        :param nachricht: [9]
        :return: Resultate
        """

        query = """
                    SELECT set_id, set_name, beschreibung, sprache, anz_downloads FROM vociset WHERE user_id = ?
                """
        self.CURSOR.execute(query, (self.eingeloggter_user_id,))
        ergebnisse = self.CURSOR.fetchall()

        return [9, ergebnisse]

    def beantworte_kid10(self, nachricht: list) -> list:
        """
        Der Client fordert die Ausführung einer Aktion (löschen) angewendet auf das Set set_id auf dem Server.
        :param nachricht: nachricht: [10, set_id, löschen]
        :return: Erfolg True/False
        """

        set_id = nachricht[1]
        aktion = nachricht[2]

        if aktion == 0:

            # print("LÖSCH AUFTRAG GEGEBEN")
            # print(f"set_id: {set_id}")
            # print(f"self.eingeloggeter_user_id: {self.eingeloggter_user_id}")

            # Query zum löschen
            # "AND user_id ..." bewirkt, dass der Eintrag nur gelöscht wird, wenn das Set dem eingeloggten User gehört,
            # was eigentlich immer der Fall ist, aber theoretisch könnte man das manipulieren.
            query = """
            DELETE FROM vociset WHERE set_id = ? AND user_id = ?
            """

            self.CURSOR.execute(query, (set_id, self.eingeloggter_user_id))

            self.DBCONN.commit()

            return [10, True]

        return [10, False]
