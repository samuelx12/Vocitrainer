# -*- coding: utf-8 -*-
"""
client.py
Das Hauptfile, aus diesem werden die anderen Dateien eingebunden.
Der Code erstellt das Hauptfenster und Startet die QT-Eventloop. Von dieser aus läuft das Programm mittels
Signalen und Slots weiter.
"""

from rich import traceback

from PyQt5.QtWidgets import QApplication
import sys
from hauptfenster import Hauptfenster
import exception
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from configobj import ConfigObj

# VERSION HIER ANPASSEN
versionen = {
    "vocitrainer": "1.0",
    "qt": QT_VERSION_STR,
    "pyqt": PYQT_VERSION_STR
}

try:
    config = ConfigObj("settings.ini")
    stil = config['Allgemein']['stil']
except:
    stil = "Vocitrainer"

print(stil)

app = QApplication(sys.argv)
if stil == "Vocitrainer":
    app.setStyle("fusion")

window = Hauptfenster(versionen)
window.show()

# Für Debugzwecke: Schönes Traceback installieren
traceback.install()

# trainingsfenster = Trainingsfenster()
# trainingsfenster.show()

# Start der Event loop
app.exec()
