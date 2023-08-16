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
from training import TestTraining


class Trainingsfenster(QDialog, Ui_Trainingsfenster):
    """
    Trainingsfenster
    """
    def __init__(self, *args, obj=None, **kwargs):
        super(Trainingsfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Training")
        # self.setCentralWidget(self.stackedWidget)
        self.stackedWidget.setCurrentIndex(0)

        # Signale mit Slots verbinden
        self.f_cmd_pruefen.clicked.connect(self.f_cmd_pruefen_clicked)
        self.f_cmd_abbrechen.clicked.connect(self.f_cmd_abbrechen_clicked)
        self.a_cmd_weiter.clicked.connect(self.a_cmd_weiter_clicked)
        self.a_cmd_abbrechen.clicked.connect(self.a_cmd_abbrechen_clicked)

        # Training Controller laden
        self.controler = TestTraining()

        # Erste Frage laden
        self.frage_laden()

    def frage_laden(self):
        # Frage Info vom Kontroller empfangen
        frage = self.controler.frage()
        self.f_lbl_deutsch_wort.setText(frage[0])

    def f_cmd_pruefen_clicked(self):
        """PRÜFEN geklickt"""
        antwort = self.controler.antwort(self.f_txt_fremdsprache.text())
        self.a_lbl_deutsch_wort.setText(antwort[0])
        self.a_lbl_fremdsprache_wort.setText(antwort[1])
        self.a_lbl_deutsch_beschreibung.setText(str(antwort[2]))
        self.stackedWidget.setCurrentIndex(1)

    def f_cmd_abbrechen_clicked(self):
        self.close()

    def a_cmd_weiter_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    def a_cmd_abbrechen_clicked(self):
        self.close()
