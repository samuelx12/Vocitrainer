# -*- coding: utf-8 -*-
"""
client.py
Das Hauptfile, aus diesem werden die anderen Dateien eingebunden.
Der Code erstellt das Hauptfenster und startet die QT-Eventloop. Von dieser aus läuft das Programm mittels
Signalen und Slots weiter.
"""

from rich import traceback
from PyQt5.QtWidgets import QApplication, QStyleFactory
import sys
from hauptfenster import Hauptfenster
import exception
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from configobj import ConfigObj

# Für Debugzwecke: Schönes Traceback installieren
traceback.install()

# VERSION HIER ANPASSEN
versionen = {
    "vocitrainer": "v1.0.0-alpha",
    "qt": QT_VERSION_STR,
    "pyqt": PYQT_VERSION_STR
}

try:
    config = ConfigObj("settings.ini")
    stil = config['Allgemein']['stil']
except:
    stil = "Vocitrainer"

app = QApplication(sys.argv)

if stil == "Vocitrainer":
    app.setStyle("fusion")
elif stil == "Windows":
    app.setStyle("WindowsVista")
elif stil == "Nostalgisch":
    app.setStyle("Windows")

window = Hauptfenster(versionen, app)
window.show()

# Start der Event loop
exit_code = app.exec_()
sys.exit(exit_code)
