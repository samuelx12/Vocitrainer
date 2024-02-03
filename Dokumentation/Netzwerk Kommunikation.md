# Netzwerkkommunikation

Ich brauche für die Kommunikation zwischen Server und Client die Python Standartbibliothek `socket`. Mit dieser Bibliothek baut der Server mit dem Client eine eigene Verbindung auf, was wichtig ist für die Authentifizierung.
Konkret nutze ich die Standartlibrary `pickle`. Mit dieser kann man Python Objekte seriealisieren, was es möglich macht, diese mit `socket`zu versenden.

Ich versende in meiner Anwendung immer Python Listen in welcher das erste Element eine Ganzzahl ist, welche bezeichnet, was danach in der Liste kommt (quasi ein eigenes Miniprotokoll). Ich nenne diese Zahl: kommunikations_id. Hier eine Auflistung aller Kommunikations IDs

- 1: Verbindung wird beendent
- 2: unbenutzt
- 3: Set suche / Set Resultate
- 4: Set Herunterladen
  - KID
  - set_id
- 4-Antwort: Set Herunterladen
  - KID
  - Set Datensatz
  - Liste der
    - Karte Datensätze
- 5: Login
  - KID
  - email
  - passwort (gehasht)
- 5-Antwort: Login
  - KID
  - Erfolg True/False
- 6: Registrieren
  - KID
  - benutzername
  - email
  - passwort (gehasht)
- 6-Antwort: Registrieren
  - KID
  - Ergebniss int
    - 0 = Erfolg
    - 1 = Benutzername bereits gewählt
    - 2 = E-Mail bereits registriert
    - 3 = Bestätigungsemail konnte nicht versendet werden
- 7: E-Mail-Überprüfung
  - KID
  - Erfolg
- 7-Antwort: E-Mail-Überprüfung
  - KID
  - Erfolg (True/False)
- 8: Set hochladen
  - KID
  - Set Datensatz
  - Liste der
    - Karte Datensätze
- 8-Antwort:
  - KID
  - Erfolg (True/False)
- 9: VerwaltenInfo
  - KID
- 9-Antwort: VerwaltenInfo
  - KID
  - Liste der 
    - Vociset Datensätze
    = [id, name, tags, sprache, anz_downloads]
- 10: VerwaltenExe
  - KID
  - Set_Id
  - Aktion
    - 0: Löschen
- 10-Antwort:
  - KID
  - Erfolg (True/False)

