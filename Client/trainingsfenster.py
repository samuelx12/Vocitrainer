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
from ui_trainingsfenster import Ui_Trainingsfenster
from trainingscontroller import TestTraining, TC_Einfach


class Trainingsfenster(QDialog, Ui_Trainingsfenster):
    """
    Trainingsfenster
    """
    def __init__(self, *args, obj=None, **kwargs):
        super(Trainingsfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Training")

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite * 4/12), int(hoehe * 3/8), int(breite * 1/3), int(hoehe * 1/6))

        # self.setCentralWidget(self.stackedWidget)
        self.stackedWidget.setCurrentIndex(0)

        # Signale mit Slots verbinden
        self.f_cmd_pruefen.clicked.connect(self.f_cmd_pruefen_clicked)
        self.f_cmd_abbrechen.clicked.connect(self.f_cmd_abbrechen_clicked)
        self.a_cmd_weiter.clicked.connect(self.a_cmd_weiter_clicked)
        self.a_cmd_abbrechen.clicked.connect(self.a_cmd_abbrechen_clicked)

        # Training Controller laden
        self.controller = TC_Einfach()

        # Erste Frage laden
        self.frage_laden()

        self.setStyleSheet(
            """font: 14pt "MS Shell Dlg 2";"""
        )

    def frage_laden(self):
        # Frage Info vom Kontroller empfangen
        frage = self.controller.frage()
        self.f_txt_fremdsprache.setText("")

        self.f_lbl_deutsch_wort.setText(frage[0][1])

    def f_cmd_pruefen_clicked(self):
        """PRÜFEN GEKLICKT"""
        antwort = self.controller.antwort(self.f_txt_fremdsprache.text())
        self.a_lbl_deutsch_wort.setText(antwort[0][1])
        self.a_lbl_fremdsprache_wort.setText(antwort[0][2])
        self.a_lbl_deutsch_beschreibung.setText(str(antwort[1]))
        if antwort[1]:
            self.a_lbl_fremdsprache_wort.setStyleSheet(
                """
                background-color: rgb(197, 225, 196);
                border: 3px solid;
                border-radius: 3px;
                border-color: rgb(197, 225, 196);
                """
            )
        else:
            self.a_lbl_fremdsprache_wort.setStyleSheet(
                """
                background-color: rgb(225, 171, 171);
                border: 3px solid;
                border-radius: 3px;
                border-color: rgb(225, 171, 171);
                """
            )
        self.stackedWidget.setCurrentIndex(1)

    def f_cmd_abbrechen_clicked(self):
        """ABBRECHEN (F) GEKLICKT"""
        self.close()

    def a_cmd_weiter_clicked(self):
        """WEITER GEKLICKT"""
        self.frage_laden()
        self.stackedWidget.setCurrentIndex(0)

    def a_cmd_abbrechen_clicked(self):
        """ABBRECHEN (A) GEKLICKT"""
        self.close()
