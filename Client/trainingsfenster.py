# -*- coding: utf-8 -*-
"""
trainingsfenster.py
Diese Datei enthält eigentlich nur die Klasse Trainingsfenster, welche von QMainWindow erbt. Das Hauptfenster ist das erste
Fenster, welches aufgeht. Das Programm läuft weiter, wenn Signale auftreten, welche mit einem Slot (Funktion) verbunden
wurden (Qt-Konzept)
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from models import KartenModel
from PyQt5.uic import loadUi
import sqlite3
from ui_trainingsfenster import Ui_Trainingsfenster


class Trainingsfenster(QMainWindow, Ui_Trainingsfenster):
    """
    Trainingsfenster
    """
    def __init__(self, *args, obj=None, **kwargs):
        super(Trainingsfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Training")
        self.setCentralWidget(self.stackedWidget)
        self.stackedWidget.setCurrentIndex(0)
