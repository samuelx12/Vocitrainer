# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trainingsfenster.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Trainingsfenster(object):
    def setupUi(self, Trainingsfenster):
        Trainingsfenster.setObjectName("Trainingsfenster")
        Trainingsfenster.resize(585, 423)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Trainingsfenster.setWindowIcon(icon)
        Trainingsfenster.setLayoutDirection(QtCore.Qt.LeftToRight)
        Trainingsfenster.setStyleSheet("")
        Trainingsfenster.setSizeGripEnabled(False)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Trainingsfenster)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.stackedWidget = QtWidgets.QStackedWidget(Trainingsfenster)
        self.stackedWidget.setObjectName("stackedWidget")
        self.frage_page = QtWidgets.QWidget()
        self.frage_page.setObjectName("frage_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frage_page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.f_lbl_deutsch_beschreibung = QtWidgets.QLabel(self.frage_page)
        self.f_lbl_deutsch_beschreibung.setObjectName("f_lbl_deutsch_beschreibung")
        self.verticalLayout.addWidget(self.f_lbl_deutsch_beschreibung)
        self.f_lbl_deutsch_wort = QtWidgets.QLabel(self.frage_page)
        self.f_lbl_deutsch_wort.setStyleSheet("background-color: rgb(201, 220, 225);\n"
"border: 3px solid;\n"
"border-radius: 3px;\n"
"border-color: rgb(201, 220, 225);")
        self.f_lbl_deutsch_wort.setWordWrap(True)
        self.f_lbl_deutsch_wort.setObjectName("f_lbl_deutsch_wort")
        self.verticalLayout.addWidget(self.f_lbl_deutsch_wort)
        self.f_lbl_fremdsprache = QtWidgets.QLabel(self.frage_page)
        self.f_lbl_fremdsprache.setObjectName("f_lbl_fremdsprache")
        self.verticalLayout.addWidget(self.f_lbl_fremdsprache)
        self.f_txt_fremdsprache = QtWidgets.QLineEdit(self.frage_page)
        self.f_txt_fremdsprache.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.f_txt_fremdsprache.setObjectName("f_txt_fremdsprache")
        self.verticalLayout.addWidget(self.f_txt_fremdsprache)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.frage_page)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.f_cmd_pruefen = QtWidgets.QPushButton(self.frage_page)
        self.f_cmd_pruefen.setObjectName("f_cmd_pruefen")
        self.horizontalLayout.addWidget(self.f_cmd_pruefen)
        self.f_cmd_abbrechen = QtWidgets.QPushButton(self.frage_page)
        self.f_cmd_abbrechen.setObjectName("f_cmd_abbrechen")
        self.horizontalLayout.addWidget(self.f_cmd_abbrechen)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.stackedWidget.addWidget(self.frage_page)
        self.antwort_page = QtWidgets.QWidget()
        self.antwort_page.setObjectName("antwort_page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.antwort_page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.a_lbl_deutsch_beschreibung = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_deutsch_beschreibung.setObjectName("a_lbl_deutsch_beschreibung")
        self.verticalLayout_2.addWidget(self.a_lbl_deutsch_beschreibung)
        self.a_lbl_deutsch_wort = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_deutsch_wort.setStyleSheet("background-color: rgb(201, 220, 225);\n"
"border: 3px solid;\n"
"border-radius: 3px;\n"
"border-color: rgb(201, 220, 225);")
        self.a_lbl_deutsch_wort.setObjectName("a_lbl_deutsch_wort")
        self.verticalLayout_2.addWidget(self.a_lbl_deutsch_wort)
        self.a_lbl_deineAntwort_beschreibung = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_deineAntwort_beschreibung.setObjectName("a_lbl_deineAntwort_beschreibung")
        self.verticalLayout_2.addWidget(self.a_lbl_deineAntwort_beschreibung)
        self.a_lbl_deineAntwort_wort = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_deineAntwort_wort.setStyleSheet("background-color: rgb(225, 171, 171);\n"
"border: 3px solid;\n"
"border-radius: 3px;\n"
"border-color: rgb(225, 171, 171);")
        self.a_lbl_deineAntwort_wort.setObjectName("a_lbl_deineAntwort_wort")
        self.verticalLayout_2.addWidget(self.a_lbl_deineAntwort_wort)
        self.a_lbl_fremdsprache_beschreibung = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_fremdsprache_beschreibung.setObjectName("a_lbl_fremdsprache_beschreibung")
        self.verticalLayout_2.addWidget(self.a_lbl_fremdsprache_beschreibung)
        self.a_lbl_fremdsprache_wort = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_fremdsprache_wort.setStyleSheet("background-color: rgb(197, 225, 196);\n"
"border: 3px solid;\n"
"border-radius: 3px;\n"
"border-color: rgb(197, 225, 196);")
        self.a_lbl_fremdsprache_wort.setObjectName("a_lbl_fremdsprache_wort")
        self.verticalLayout_2.addWidget(self.a_lbl_fremdsprache_wort)
        self.a_lbl_definition_beschreibung = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_definition_beschreibung.setObjectName("a_lbl_definition_beschreibung")
        self.verticalLayout_2.addWidget(self.a_lbl_definition_beschreibung)
        self.a_lbl_definition_wort = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_definition_wort.setWordWrap(True)
        self.a_lbl_definition_wort.setObjectName("a_lbl_definition_wort")
        self.verticalLayout_2.addWidget(self.a_lbl_definition_wort)
        self.a_lbl_bemerkung_beschreibung = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_bemerkung_beschreibung.setObjectName("a_lbl_bemerkung_beschreibung")
        self.verticalLayout_2.addWidget(self.a_lbl_bemerkung_beschreibung)
        self.a_lbl_bemerkung_wort = QtWidgets.QLabel(self.antwort_page)
        self.a_lbl_bemerkung_wort.setWordWrap(True)
        self.a_lbl_bemerkung_wort.setObjectName("a_lbl_bemerkung_wort")
        self.verticalLayout_2.addWidget(self.a_lbl_bemerkung_wort)
        spacerItem2 = QtWidgets.QSpacerItem(17, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.label_2 = QtWidgets.QLabel(self.antwort_page)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.a_cmd_weiter = QtWidgets.QPushButton(self.antwort_page)
        self.a_cmd_weiter.setObjectName("a_cmd_weiter")
        self.horizontalLayout_2.addWidget(self.a_cmd_weiter)
        self.a_cmd_abbrechen = QtWidgets.QPushButton(self.antwort_page)
        self.a_cmd_abbrechen.setObjectName("a_cmd_abbrechen")
        self.horizontalLayout_2.addWidget(self.a_cmd_abbrechen)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.stackedWidget.addWidget(self.antwort_page)
        self.zeigen_page = QtWidgets.QWidget()
        self.zeigen_page.setObjectName("zeigen_page")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.zeigen_page)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.z_lbl_NeuesWort = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_NeuesWort.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.z_lbl_NeuesWort.setObjectName("z_lbl_NeuesWort")
        self.horizontalLayout_4.addWidget(self.z_lbl_NeuesWort)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.line = QtWidgets.QFrame(self.zeigen_page)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout_4.addWidget(self.line)
        self.z_lbl_ProfiTipp = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_ProfiTipp.setMinimumSize(QtCore.QSize(300, 0))
        self.z_lbl_ProfiTipp.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";")
        self.z_lbl_ProfiTipp.setWordWrap(True)
        self.z_lbl_ProfiTipp.setObjectName("z_lbl_ProfiTipp")
        self.horizontalLayout_4.addWidget(self.z_lbl_ProfiTipp)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.z_lbl_deutsch_beschreibung = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_deutsch_beschreibung.setObjectName("z_lbl_deutsch_beschreibung")
        self.verticalLayout_4.addWidget(self.z_lbl_deutsch_beschreibung)
        self.z_lbl_deutsch_wort = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_deutsch_wort.setStyleSheet("background-color: rgb(201, 220, 225);\n"
"border: 3px solid;\n"
"border-radius: 3px;\n"
"border-color: rgb(201, 220, 225);")
        self.z_lbl_deutsch_wort.setObjectName("z_lbl_deutsch_wort")
        self.verticalLayout_4.addWidget(self.z_lbl_deutsch_wort)
        self.z_lbl_fremdsprache_beschreibung = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_fremdsprache_beschreibung.setObjectName("z_lbl_fremdsprache_beschreibung")
        self.verticalLayout_4.addWidget(self.z_lbl_fremdsprache_beschreibung)
        self.z_lbl_fremdsprache_wort = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_fremdsprache_wort.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(184, 225, 210);\n"
"border: 3px solid;\n"
"border-radius: 3px;\n"
"border-color: rgb(184, 225, 210);")
        self.z_lbl_fremdsprache_wort.setObjectName("z_lbl_fremdsprache_wort")
        self.verticalLayout_4.addWidget(self.z_lbl_fremdsprache_wort)
        self.z_lbl_definition_beschreibung = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_definition_beschreibung.setObjectName("z_lbl_definition_beschreibung")
        self.verticalLayout_4.addWidget(self.z_lbl_definition_beschreibung)
        self.z_lbl_definition_wort = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_definition_wort.setWordWrap(True)
        self.z_lbl_definition_wort.setObjectName("z_lbl_definition_wort")
        self.verticalLayout_4.addWidget(self.z_lbl_definition_wort)
        self.z_lbl_bemerkung_beschreibung = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_bemerkung_beschreibung.setObjectName("z_lbl_bemerkung_beschreibung")
        self.verticalLayout_4.addWidget(self.z_lbl_bemerkung_beschreibung)
        self.z_lbl_bemerkung_wort = QtWidgets.QLabel(self.zeigen_page)
        self.z_lbl_bemerkung_wort.setWordWrap(True)
        self.z_lbl_bemerkung_wort.setObjectName("z_lbl_bemerkung_wort")
        self.verticalLayout_4.addWidget(self.z_lbl_bemerkung_wort)
        spacerItem5 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem5)
        self.label_3 = QtWidgets.QLabel(self.zeigen_page)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.z_cmd_weiter = QtWidgets.QPushButton(self.zeigen_page)
        self.z_cmd_weiter.setObjectName("z_cmd_weiter")
        self.horizontalLayout_3.addWidget(self.z_cmd_weiter)
        self.z_cmd_abbrechen = QtWidgets.QPushButton(self.zeigen_page)
        self.z_cmd_abbrechen.setObjectName("z_cmd_abbrechen")
        self.horizontalLayout_3.addWidget(self.z_cmd_abbrechen)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.stackedWidget.addWidget(self.zeigen_page)
        self.verticalLayout_3.addWidget(self.stackedWidget)

        self.retranslateUi(Trainingsfenster)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Trainingsfenster)

    def retranslateUi(self, Trainingsfenster):
        _translate = QtCore.QCoreApplication.translate
        Trainingsfenster.setWindowTitle(_translate("Trainingsfenster", "Dialog"))
        self.f_lbl_deutsch_beschreibung.setText(_translate("Trainingsfenster", "Deutsch:"))
        self.f_lbl_deutsch_wort.setText(_translate("Trainingsfenster", "TextLabel"))
        self.f_lbl_fremdsprache.setText(_translate("Trainingsfenster", "Fremdsprache:"))
        self.label.setText(_translate("Trainingsfenster", "Frage"))
        self.f_cmd_pruefen.setText(_translate("Trainingsfenster", "Prüfen"))
        self.f_cmd_abbrechen.setText(_translate("Trainingsfenster", "Abbrechen"))
        self.a_lbl_deutsch_beschreibung.setText(_translate("Trainingsfenster", "Deutsch:"))
        self.a_lbl_deutsch_wort.setText(_translate("Trainingsfenster", "TextLabel"))
        self.a_lbl_deineAntwort_beschreibung.setText(_translate("Trainingsfenster", "Deine Antwort:"))
        self.a_lbl_deineAntwort_wort.setText(_translate("Trainingsfenster", "TextLabel"))
        self.a_lbl_fremdsprache_beschreibung.setText(_translate("Trainingsfenster", "Fremdsprache:"))
        self.a_lbl_fremdsprache_wort.setText(_translate("Trainingsfenster", "TextLabel"))
        self.a_lbl_definition_beschreibung.setText(_translate("Trainingsfenster", "Definition:"))
        self.a_lbl_definition_wort.setText(_translate("Trainingsfenster", "DEFINTION DEFINITION DEFINTION aösdlfkjasdfljasdlöfkj aölskdjf alökdsfj aölsfj aösldkfj aösdlkfj alösdkfj aölsdkfj aölsdkfj aölsdkfj aölsdkfj aölkdsfj aöllskdjf aölskdfj aölskdfj aölskdjf aölsdkfj aölskdfj aölskdfj aöldkfj "))
        self.a_lbl_bemerkung_beschreibung.setText(_translate("Trainingsfenster", "Bemerkung:"))
        self.a_lbl_bemerkung_wort.setText(_translate("Trainingsfenster", "BEMERKUNG BEMERKUNG BEMERKUNG"))
        self.label_2.setText(_translate("Trainingsfenster", "Antwort"))
        self.a_cmd_weiter.setText(_translate("Trainingsfenster", "Weiter"))
        self.a_cmd_abbrechen.setText(_translate("Trainingsfenster", "Abbrechen"))
        self.z_lbl_NeuesWort.setText(_translate("Trainingsfenster", "Neues Wort!"))
        self.z_lbl_ProfiTipp.setText(_translate("Trainingsfenster", "Profi-Tipp: Schreibe das Wort einmal von Hand ab. Das hilft, es sich schnell zu merken."))
        self.z_lbl_deutsch_beschreibung.setText(_translate("Trainingsfenster", "Deutsch:"))
        self.z_lbl_deutsch_wort.setText(_translate("Trainingsfenster", "TextLabel"))
        self.z_lbl_fremdsprache_beschreibung.setText(_translate("Trainingsfenster", "Fremdsprache:"))
        self.z_lbl_fremdsprache_wort.setText(_translate("Trainingsfenster", "TextLabel"))
        self.z_lbl_definition_beschreibung.setText(_translate("Trainingsfenster", "Definition:"))
        self.z_lbl_definition_wort.setText(_translate("Trainingsfenster", "DEFINTION DEFINITION DEFINTION aösdlfkjasdfljasdlöfkj aölskdjf alökdsfj aölsfj aösldkfj aösdlkfj alösdkfj aölsdkfj aölsdkfj aölsdkfj aölsdkfj aölkdsfj aöllskdjf aölskdfj aölskdfj aölskdjf aölsdkfj aölskdfj aölskdfj aöldkfj "))
        self.z_lbl_bemerkung_beschreibung.setText(_translate("Trainingsfenster", "Bemerkung:"))
        self.z_lbl_bemerkung_wort.setText(_translate("Trainingsfenster", "BEMERKUNG BEMERKUNG BEMERKUNG"))
        self.label_3.setText(_translate("Trainingsfenster", "Zeigen"))
        self.z_cmd_weiter.setText(_translate("Trainingsfenster", "Weiter"))
        self.z_cmd_abbrechen.setText(_translate("Trainingsfenster", "Abbrechen"))
