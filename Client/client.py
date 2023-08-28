# -*- coding: utf-8 -*-
"""
client.py
Das Hauptfile, aus diesem werden die anderen Dateien eingebunden.
Der Code erstellt das Hauptfenster und Startet die QT-Eventloop. Von dieser aus läuft das Programm mittels
Signalen und Slots weiter.
"""

from PyQt5.QtWidgets import QApplication
import sys
from hauptfenster import Hauptfenster
from trainingsfenster import Trainingsfenster
import exception
from rich import traceback

# Für Debugzwecke: Schönes Traceback installieren
traceback.install()

app = QApplication(sys.argv)
app.setStyle("fusion")

window = Hauptfenster()
window.show()

# trainingsfenster = Trainingsfenster()
# trainingsfenster.show()

# Start der Event loop
app.exec()
