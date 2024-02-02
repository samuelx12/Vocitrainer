# Dokumentation Programmstruktur

## Client
Für den Start des Vocitrainers muss die Datei `client.py` ausgeführt werden.
### `client.py`:
Einige Einstellungen und Informationen werden geladen und das Hauptfenster wird von `hauptfenster.py` importiert und gestartet (In Qt verwaltet das 'Fenster' die EventLoop)

### `hauptfenster.py`:
Das ist mit über 1000 Zeilen die länste Datei im ganzen Projekt. In ihr ist das Hauptfenster definiert.

Vom Hauptfenster aus werden auch alle anderen Fenster importiert und gestartet. Dabei hat jedes Fenster seine eigene Klasse welche in einer eigenen Datei definiert ist.

### `network.py`:
Die Klasse Network ein Abstratkionslayer damit man im Code des Fensters nicht direkt mit den Kommunikations IDs und der Verbindung auseinandersetzen muss. Sie bietet dafür eine Methode für jede Aufgabe, welche der Server erfüllt. Diese sind alle dort beschrieben.

### `models.py`:
Diese Datei enthält das Model für die Tabelle im Hauptfenster. Dabei handelt es sich um eine Komponente des Model-View Konzeptes, welches Qt hat.

### `trainingsfenster.py` und `trainingscontroller.py`:
Fürs Lernen geht ein eigenes Fenster auf, welches in trainings**fenster**.py beschrieben ist.

Die Logik des Lernalgorithmus ist jedoch vom Fenster getrennt und in der eigenen Datei trainigs**controller**.py programmiert.

### `ressources_rc.py`:
Diese Datei ist vom Qt-Resource-Compiler kompiliert. Sie enthält die Bilder und die Logos. Das Qt Ressource System verwaltet die Bilder so, damit beim Packaging keine Fehler mit nicht gefundenen Bildern auftreten.

### `res/`:
Hier ist vielleicht zu dem Management und Workflow vom erstellen von Fenstern notwenig:
Die Fenster werdem im QtDesigner zusammengestellt und in einer .ui-Datei gespeichert. Diese kompiliere ich mit dem pyuic5 Skript zu ui_*****.py Dateien. Diese werden dann von den Datein in denen die Fenster beschrieben sind importiert. So lässt sich gut die Funktionalität vom Aussehen trennen. Zudem lassen sich so die Fenster ohne Codeverlust erneut kompilieren.

## Server
Der Server ist relativ simpel aufgebaut.
Die auszuführende Datei ist `server.py`. Sie startet den Server und nimmt ab dann Verbindungen an, welche in einem eigenen Thread behandelt werden.

Diese Thread Klasse "Session" ist in `session.py` beschrieben.
