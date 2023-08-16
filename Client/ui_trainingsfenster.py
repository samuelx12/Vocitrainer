# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trainingsfensterphnYJg.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Trainingsfenster(object):
    def setupUi(self, Trainingsfenster):
        if not Trainingsfenster.objectName():
            Trainingsfenster.setObjectName(u"Trainingsfenster")
        Trainingsfenster.resize(443, 290)
        Trainingsfenster.setLayoutDirection(Qt.LeftToRight)
        Trainingsfenster.setSizeGripEnabled(False)
        self.verticalLayout_3 = QVBoxLayout(Trainingsfenster)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stackedWidget = QStackedWidget(Trainingsfenster)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.frage_page = QWidget()
        self.frage_page.setObjectName(u"frage_page")
        self.verticalLayout = QVBoxLayout(self.frage_page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.f_lbl_deutsch_beschreibung = QLabel(self.frage_page)
        self.f_lbl_deutsch_beschreibung.setObjectName(u"f_lbl_deutsch_beschreibung")

        self.verticalLayout.addWidget(self.f_lbl_deutsch_beschreibung)

        self.f_lbl_deutsch_wort = QLabel(self.frage_page)
        self.f_lbl_deutsch_wort.setObjectName(u"f_lbl_deutsch_wort")
        self.f_lbl_deutsch_wort.setStyleSheet(u"background-color: rgb(201, 220, 225);\n"
"border: 3px solid;\n"
"border-radius: 3px;\n"
"border-color: rgb(201, 220, 225);")

        self.verticalLayout.addWidget(self.f_lbl_deutsch_wort)

        self.f_lbl_fremdsprache = QLabel(self.frage_page)
        self.f_lbl_fremdsprache.setObjectName(u"f_lbl_fremdsprache")

        self.verticalLayout.addWidget(self.f_lbl_fremdsprache)

        self.f_txt_fremdsprache = QLineEdit(self.frage_page)
        self.f_txt_fremdsprache.setObjectName(u"f_txt_fremdsprache")
        self.f_txt_fremdsprache.setCursorMoveStyle(Qt.LogicalMoveStyle)

        self.verticalLayout.addWidget(self.f_txt_fremdsprache)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.f_cmd_pruefen = QPushButton(self.frage_page)
        self.f_cmd_pruefen.setObjectName(u"f_cmd_pruefen")

        self.horizontalLayout.addWidget(self.f_cmd_pruefen)

        self.f_cmd_abbrechen = QPushButton(self.frage_page)
        self.f_cmd_abbrechen.setObjectName(u"f_cmd_abbrechen")

        self.horizontalLayout.addWidget(self.f_cmd_abbrechen)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(self.frage_page)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.stackedWidget.addWidget(self.frage_page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_2 = QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.a_lbl_deutsch_beschreibung = QLabel(self.page_2)
        self.a_lbl_deutsch_beschreibung.setObjectName(u"a_lbl_deutsch_beschreibung")

        self.verticalLayout_2.addWidget(self.a_lbl_deutsch_beschreibung)

        self.a_lbl_deutsch_wort = QLabel(self.page_2)
        self.a_lbl_deutsch_wort.setObjectName(u"a_lbl_deutsch_wort")
        self.a_lbl_deutsch_wort.setStyleSheet(u"background-color: rgb(201, 220, 225);\n"
"border: 3px solid;\n"
"border-radius: 3px;\n"
"border-color: rgb(201, 220, 225);")

        self.verticalLayout_2.addWidget(self.a_lbl_deutsch_wort)

        self.a_lbl_fremdsprache_beschreibung = QLabel(self.page_2)
        self.a_lbl_fremdsprache_beschreibung.setObjectName(u"a_lbl_fremdsprache_beschreibung")

        self.verticalLayout_2.addWidget(self.a_lbl_fremdsprache_beschreibung)

        self.a_lbl_fremdsprache_wort = QLabel(self.page_2)
        self.a_lbl_fremdsprache_wort.setObjectName(u"a_lbl_fremdsprache_wort")
        self.a_lbl_fremdsprache_wort.setStyleSheet(u"background-color: rgb(201, 220, 225);\n"
"border: 3px solid;\n"
"border-radius: 3px;\n"
"border-color: rgb(201, 220, 225);")

        self.verticalLayout_2.addWidget(self.a_lbl_fremdsprache_wort)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.a_cmd_weiter = QPushButton(self.page_2)
        self.a_cmd_weiter.setObjectName(u"a_cmd_weiter")

        self.horizontalLayout_2.addWidget(self.a_cmd_weiter)

        self.a_cmd_abbrechen = QPushButton(self.page_2)
        self.a_cmd_abbrechen.setObjectName(u"a_cmd_abbrechen")

        self.horizontalLayout_2.addWidget(self.a_cmd_abbrechen)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.retranslateUi(Trainingsfenster)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Trainingsfenster)
    # setupUi

    def retranslateUi(self, Trainingsfenster):
        Trainingsfenster.setWindowTitle(QCoreApplication.translate("Trainingsfenster", u"Dialog", None))
        self.f_lbl_deutsch_beschreibung.setText(QCoreApplication.translate("Trainingsfenster", u"Deutsch:", None))
        self.f_lbl_deutsch_wort.setText(QCoreApplication.translate("Trainingsfenster", u"TextLabel", None))
        self.f_lbl_fremdsprache.setText(QCoreApplication.translate("Trainingsfenster", u"Fremdsprache:", None))
        self.f_cmd_pruefen.setText(QCoreApplication.translate("Trainingsfenster", u"Pr\u00fcfen", None))
        self.f_cmd_abbrechen.setText(QCoreApplication.translate("Trainingsfenster", u"Abbrechen", None))
        self.label.setText(QCoreApplication.translate("Trainingsfenster", u"Frage", None))
        self.a_lbl_deutsch_beschreibung.setText(QCoreApplication.translate("Trainingsfenster", u"Deutsch:", None))
        self.a_lbl_deutsch_wort.setText(QCoreApplication.translate("Trainingsfenster", u"TextLabel", None))
        self.a_lbl_fremdsprache_beschreibung.setText(QCoreApplication.translate("Trainingsfenster", u"Fremdsprache:", None))
        self.a_lbl_fremdsprache_wort.setText(QCoreApplication.translate("Trainingsfenster", u"TextLabel", None))
        self.a_cmd_weiter.setText(QCoreApplication.translate("Trainingsfenster", u"Weiter", None))
        self.a_cmd_abbrechen.setText(QCoreApplication.translate("Trainingsfenster", u"Abbrechen", None))
        self.label_2.setText(QCoreApplication.translate("Trainingsfenster", u"Antwort", None))
    # retranslateUi

