# Netzwerkkommunikation

Ich brauche für die Kommunikation zwischen Server und Client die Python Standartbibliothek `socket`. Mit dieser Bibliothek baut der Server mit dem Client eine eigene Verbindung auf, was wichtig ist für die Authentifizierung.
Konkret nutze ich die Standartlibrary `pickle`. Mit dieser kann man Python Objekte seriealisieren, was es möglich macht, diese mit `socket`zu versenden.

Ich versende in meiner Anwendung immer Python Listen in welcher das erste Element eine Ganzzahl ist, welche bezeichnet, was danach in der Liste kommt. Ich nenne diese Zahl: kommunikations_id. Hier eine Auflistung aller Kommunikations IDs

- 1: Verbindung wird beendent
- 2: Authentifizierung
- 3: Set suche
- 