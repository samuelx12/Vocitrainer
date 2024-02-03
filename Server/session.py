# -*- coding: utf-8 -*-
"""
session.py
Hier ist der Thread für die Session des Servers mit dem Client
"""

import threading
import ssl
import pickle
import time
from typing import List
from datetime import datetime
import sqlite3
from rich import print as rprint
import email_helper
import random


class Session(threading.Thread):
    """
    Damit mehrere Clients gleichzeitig vom Server verarbeitet werden können, werden Clients in Threads behandelt.
    Ausgeführt wird die run()-Methode.
    Sie besteht aus einer Endlosschleife:
        1. Auf Nachricht von Client warten
        2. Kommunikations ID der Nachricht ermitteln (Beschrieben in 'Dokumentation/Netzwerk_Kommunikation.md'
        3. Je nach Kommunikations ID die ensprechende Funktion aufrufen, welche die Anforderung dann bearbeitet
        4. Antwort versenden
    """

    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

        # Konstanten
        self.HEADER = 128
        self.FORMAT = 'utf-8'
        self.SALT = b'\xcd\xae\xd1C\xc0#a\x8ch\x83\x95\xc5%l\xc7\x14'

        # Variabeln für Registrierungsinformationen falls sich der Benutzer registrieren möchte
        self.reg_code: int = -1
        self.reg_email = ""
        self.reg_benutzername = ""
        self.reg_passwort = ""

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

        # # Zuerst Verbindung verschlüsseln (momentan entfernt)
        # # SSL-Kontext erstellen
        # ssl_kontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # ssl_kontext.load_cert_chain(certfile='server.crt', keyfile='server.key')
        #
        # # SSL Handshake
        # self.conn = ssl_kontext.wrap_socket(self.conn, server_side=True,)

        self.DBCONN = sqlite3.connect('serverdb.db')
        self.CURSOR = self.DBCONN.cursor()

        while self.verbunden:
            nachricht = self.empfangen()
            kid = nachricht[0]
            antwort = []

            if kid == 1:
                # Verbindung wird beendet
                rprint("[cyan]Eine Verbindung wurde geschlossen.")

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

            elif kid == 11:
                """
                Kontolöschung wird angefordert
                """

                antwort = self.beantworte_kid11(nachricht)

            else:
                antwort = ["FEHLER"]
                rprint(f"[yellow]Ungültige Request vom Client empfangen.")

            if self.verbunden:
                self.senden(antwort)

    def beantworte_kid3(self, nachricht) -> list:
        """
        Set suche:
        [kid, prompt, anzahl_resultat, sprache]
        """

        def zaehle_treffer(titel: str) -> int:
            """
            Zählt die Anzahl Wörter im Titel, die im Suchbegriff vorkommen.
            :param titel: Der Titel in dem gesucht werden soll
            :return: Die Anzahl der Wörter im Titel, die im Suchbegriff vorkommen.
            """
            gesplitteter_titel = titel.split()
            anz_treffer = sum(
                sum([wort.lower() in titel_teil.lower() for titel_teil in gesplitteter_titel])
                for wort in gesplitteter_prompt
            )
            print("Titel: ", titel, " Prompt: ", gesplitteter_prompt, " Anzahl Treffer: ", anz_treffer)
            return anz_treffer

        def trace_callback(statement):
            print("Ausgeführter SQL-Befehl:", statement)

        prompt: str = nachricht[1]
        anzahl_resultate: int = nachricht[2]
        sprache: str = nachricht[3]
        gesplitteter_prompt = prompt.split()

        # # Ausgeführte Befehle für Debug Printen
        self.DBCONN.set_trace_callback(trace_callback)

        # Suchquery erstellen
        # Die 'LIKE's suchen alle sets heraus, welche eines der Wörter des Suchprompts im Namen haben
        query = """
                    SELECT v.set_id, v.set_name, v.beschreibung, v.sprache, v.anz_downloads, u.benutzername, u.gesperrt
                    FROM vociset v
                    JOIN user u ON v.user_id = u.user_id
                    WHERE u.gesperrt=0
                    AND (set_name LIKE '%' || ? || '%'
                    OR beschreibung LIKE '%' || ? || '%'
                    OR u.benutzername LIKE '%' || ? || '%'
        """
        for i in range(len(gesplitteter_prompt) - 1):
            query += """ OR set_name LIKE '%' || ? || '%' 
            OR beschreibung LIKE '%' || ? || '%' 
            OR u.benutzername LIKE '%' || ? || '%'"""

        query += ")"

        # Filterung nach Sprache
        if sprache != "Alle":
            query += f" AND sprache='{sprache}'"

        gesplitteter_prompt_doppelt = []
        for splitter in gesplitteter_prompt:
            gesplitteter_prompt_doppelt.append(splitter)
            gesplitteter_prompt_doppelt.append(splitter)
            gesplitteter_prompt_doppelt.append(splitter)

        # print("Query: ", query, " Argumente: ", gesplitteter_prompt_doppelt)
        self.CURSOR.execute(query, gesplitteter_prompt_doppelt)
        ergebnisse = self.CURSOR.fetchmany(anzahl_resultate)

        # Entfernung von gesperrten Usern
        i = 0
        for ergebnis in ergebnisse:
            if ergebnis[6] == 1:
                ergebnisse.pop(i)
            else:
                i += 1

        # Jetzt werden die Resultate danach geordnet, wie viele Wörter des Suchprompts darin enthalten sind.
        ergebnisse.sort(
            key=lambda resultat:
            zaehle_treffer((resultat[1] + " " + resultat[2] + " " + resultat[3] + " " + resultat[5])),
            reverse=True
        )

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

        query = """SELECT user_id FROM user WHERE email = ? AND passwort = ?"""
        self.CURSOR.execute(query, (email, passwort))

        id = self.CURSOR.fetchone()

        if id:
            self.eingeloggter_user_id = id[0]
            rprint(f"[cyan]Der Benutzer mit der E-Mail '{email}' hat sich eingeloggt.")
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
        self.reg_benutzername = nachricht[1]
        self.reg_email = nachricht[2]
        self.reg_passwort = str(nachricht[3])

        # Überprüfen ob der Benutzername bereits existiert
        self.CURSOR.execute('SELECT COUNT(*) FROM user WHERE benutzername = ?', (self.reg_benutzername,))
        resultat = self.CURSOR.fetchone()
        if resultat[0] > 0:
            return [6, 1]

        # Überprüfen ob die E-Mail schon registriert ist
        self.CURSOR.execute('SELECT COUNT(*) FROM user WHERE email = ?', (self.reg_email,))
        resultat = self.CURSOR.fetchone()
        if resultat[0] > 0:
            return [6, 2]

        # Verifikationscode genierieren
        self.reg_code = random.randint(100000, 999999)

        betreff = "Bestätigungscode für Registierung des Vocitrainer-Accounts"
        text = "Danke für ihre Registrierung bei Vocitrainer.\n" + \
               "Das ist dein Bestätigungscode:\n" + \
               str(self.reg_code) + "\n\n" + \
               "Falls keine Regisrierung angefordert haben und nicht wissen, warum sie diese E-Mail erhalten, " + \
               "können sie die E-Mail einfach ignorieren."
        empfaenger = self.reg_email

        email_versendet = email_helper.email_senden(betreff, text, [empfaenger])

        if email_versendet:
            # Erfolg zurückmelden
            return [6, 0]
        else:
            # Fehler beim Versenden der E-Mail
            return [6, 3]

    def beantworte_kid7(self, nachricht: list) -> list:
        """
        E-Mail Überprüfung
        Der Client will die Registrierung abschliessen indem er den Code seiner E-Mail bestätigt.
        :param nachricht: [kid, code]
        :return: [kid, bool: erfolg]
        """
        code = nachricht[1]
        if self.reg_code == -1:
            # Keine Registierung angefordert.
            return [7, False]

        if code != self.reg_code:
            # Bestätigungscode falsch
            return [7, False]

        # Benutzer registrieren
        self.CURSOR.execute(
            f"INSERT INTO user (email, passwort, benutzername, gesperrt, erstellung) VALUES (?, ?, ?, 0, ?)",
            [self.reg_email, self.reg_passwort, self.reg_benutzername, datetime.now()]
        )

        # Benutzer einloggen
        self.eingeloggter_user_id = self.CURSOR.lastrowid

        # Änderngen speichern
        self.DBCONN.commit()

        # Info für das Terminal
        rprint(f"[cyan]Ein neuer Benutzer mit der E-Mail '{self.reg_email}' hat sich registriert.")

        return [7, True]

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

        except:
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
        :param nachricht: [10, set_id, löschen]
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

            self.CURSOR.execute("PRAGMA foreign_keys = ON")

            query = """
            DELETE FROM vociset WHERE set_id = ? AND user_id = ?
            """

            self.CURSOR.execute(query, (set_id, self.eingeloggter_user_id))

            self.DBCONN.commit()

            return [10, True]

        return [10, False]

    def beantworte_kid11(self, nachricht: list) -> list:
        """
        Der Benutzer will sein Konto löschen
        :param nachricht: [11]
        :return: bool Erfolg
        """
        if self.eingeloggter_user_id is None:
            # Niemand ist eingeloggt
            return [11, False]

        rprint(f"[cyan]Benutzer mit der ID {self.eingeloggter_user_id} löscht sein Konto.")

        self.CURSOR.execute("PRAGMA foreign_keys = ON")

        query = """
        DELETE FROM user WHERE user_id = ?
        """

        self.CURSOR.execute(query, (self.eingeloggter_user_id,))

        self.DBCONN.commit()

        return [11, True]
