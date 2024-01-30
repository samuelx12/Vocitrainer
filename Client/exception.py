# -*- coding: utf-8 -*-
"""
exception.py
In dieser Datei befindet sich ein wenig Code, der Exceptions, die geworfen werden während PyQt läuft, anzeigt.
Hier ist Code enthalten von:
>  video4 4 Debugging PyQt5 with Python Hooks
Von > Ly So
Aufgerufen am 17. August 2023
https://www.youtube.com/watch?v=hhRKiMceaeY
"""

import sys
from PyQt5 import QtWidgets


def catch_exceptions(t, val, tb):
    """
    Jede Exception auffangen und in einer QMessage Box anzeigen
    t: Exception Typ
    val: Exception Wert
    tb: Traceback
    """

    QtWidgets.QMessageBox.critical(None, "Ein Fehler ist aufgetrete!n", str(val))

    old_hook(t, val, tb)


old_hook = sys.excepthook

# Den Hook aufsetzen, jede unverarbeitete Exception aufzufangen
sys.excepthook = catch_exceptions
