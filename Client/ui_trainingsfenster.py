# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trainingsfensterVMhTZp.ui'
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
        Trainingsfenster.resize(599, 636)
        Trainingsfenster.setLayoutDirection(Qt.LeftToRight)
        self.stackedWidget = QStackedWidget(Trainingsfenster)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(50, 40, 391, 271))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.f_lbl_deutsch = QLabel(self.page)
        self.f_lbl_deutsch.setObjectName(u"f_lbl_deutsch")

        self.verticalLayout.addWidget(self.f_lbl_deutsch)

        self.f_txt_deutsch = QLineEdit(self.page)
        self.f_txt_deutsch.setObjectName(u"f_txt_deutsch")

        self.verticalLayout.addWidget(self.f_txt_deutsch)

        self.f_lbl_fremdsprache = QLabel(self.page)
        self.f_lbl_fremdsprache.setObjectName(u"f_lbl_fremdsprache")

        self.verticalLayout.addWidget(self.f_lbl_fremdsprache)

        self.f_txt_fremdsprache = QLineEdit(self.page)
        self.f_txt_fremdsprache.setObjectName(u"f_txt_fremdsprache")

        self.verticalLayout.addWidget(self.f_txt_fremdsprache)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.f_cmd_pruefen = QPushButton(self.page)
        self.f_cmd_pruefen.setObjectName(u"f_cmd_pruefen")

        self.horizontalLayout.addWidget(self.f_cmd_pruefen)

        self.f_cmd_abbrechen = QPushButton(self.page)
        self.f_cmd_abbrechen.setObjectName(u"f_cmd_abbrechen")

        self.horizontalLayout.addWidget(self.f_cmd_abbrechen)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_2 = QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 230, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(Trainingsfenster)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Trainingsfenster)
    # setupUi

    def retranslateUi(self, Trainingsfenster):
        Trainingsfenster.setWindowTitle(QCoreApplication.translate("Trainingsfenster", u"Dialog", None))
        self.f_lbl_deutsch.setText(QCoreApplication.translate("Trainingsfenster", u"Deutsch:", None))
        self.f_lbl_fremdsprache.setText(QCoreApplication.translate("Trainingsfenster", u"Fremdsprache:", None))
        self.f_cmd_pruefen.setText(QCoreApplication.translate("Trainingsfenster", u"Pr\u00fcfen", None))
        self.f_cmd_abbrechen.setText(QCoreApplication.translate("Trainingsfenster", u"Abbrechen", None))
        self.label.setText(QCoreApplication.translate("Trainingsfenster", u"Frage", None))
        self.label_2.setText(QCoreApplication.translate("Trainingsfenster", u"Antwort", None))
    # retranslateUi

