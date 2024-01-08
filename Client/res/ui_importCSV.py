# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importCSV.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImportCSV(object):
    def setupUi(self, ImportCSV):
        ImportCSV.setObjectName("ImportCSV")
        ImportCSV.resize(714, 657)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/icons/csv_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ImportCSV.setWindowIcon(icon)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ImportCSV)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl_Titel = QtWidgets.QLabel(ImportCSV)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lbl_Titel.setFont(font)
        self.lbl_Titel.setObjectName("lbl_Titel")
        self.verticalLayout_3.addWidget(self.lbl_Titel)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.lbl_name = QtWidgets.QLabel(ImportCSV)
        self.lbl_name.setObjectName("lbl_name")
        self.horizontalLayout_8.addWidget(self.lbl_name)
        self.txt_name = QtWidgets.QLineEdit(ImportCSV)
        self.txt_name.setObjectName("txt_name")
        self.horizontalLayout_8.addWidget(self.txt_name)
        self.lbl_sprache = QtWidgets.QLabel(ImportCSV)
        self.lbl_sprache.setObjectName("lbl_sprache")
        self.horizontalLayout_8.addWidget(self.lbl_sprache)
        self.cmb_sprache = QtWidgets.QComboBox(ImportCSV)
        self.cmb_sprache.setObjectName("cmb_sprache")
        self.cmb_sprache.addItem("")
        self.cmb_sprache.addItem("")
        self.cmb_sprache.addItem("")
        self.cmb_sprache.addItem("")
        self.cmb_sprache.addItem("")
        self.horizontalLayout_8.addWidget(self.cmb_sprache)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.lbl_beschreibung = QtWidgets.QLabel(ImportCSV)
        self.lbl_beschreibung.setObjectName("lbl_beschreibung")
        self.horizontalLayout_10.addWidget(self.lbl_beschreibung)
        self.txt_beschreibung = QtWidgets.QLineEdit(ImportCSV)
        self.txt_beschreibung.setObjectName("txt_beschreibung")
        self.horizontalLayout_10.addWidget(self.txt_beschreibung)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.line_2 = QtWidgets.QFrame(ImportCSV)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_pfad = QtWidgets.QLabel(ImportCSV)
        self.lbl_pfad.setObjectName("lbl_pfad")
        self.horizontalLayout.addWidget(self.lbl_pfad)
        self.txt_pfad = QtWidgets.QLineEdit(ImportCSV)
        self.txt_pfad.setObjectName("txt_pfad")
        self.horizontalLayout.addWidget(self.txt_pfad)
        self.cmd_durchsuchen = QtWidgets.QPushButton(ImportCSV)
        self.cmd_durchsuchen.setFlat(False)
        self.cmd_durchsuchen.setObjectName("cmd_durchsuchen")
        self.horizontalLayout.addWidget(self.cmd_durchsuchen)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.lbl_FehlerPfad = QtWidgets.QLabel(ImportCSV)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setItalic(True)
        self.lbl_FehlerPfad.setFont(font)
        self.lbl_FehlerPfad.setStyleSheet("color: rgb(170, 0, 0);")
        self.lbl_FehlerPfad.setObjectName("lbl_FehlerPfad")
        self.verticalLayout_3.addWidget(self.lbl_FehlerPfad)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbl_Vorschau = QtWidgets.QLabel(ImportCSV)
        self.lbl_Vorschau.setObjectName("lbl_Vorschau")
        self.horizontalLayout_4.addWidget(self.lbl_Vorschau)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.txt_Vorschau = QtWidgets.QTextEdit(ImportCSV)
        self.txt_Vorschau.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.txt_Vorschau.setReadOnly(True)
        self.txt_Vorschau.setObjectName("txt_Vorschau")
        self.verticalLayout_2.addWidget(self.txt_Vorschau)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_trennzeichen = QtWidgets.QLabel(ImportCSV)
        self.lbl_trennzeichen.setObjectName("lbl_trennzeichen")
        self.horizontalLayout_3.addWidget(self.lbl_trennzeichen)
        self.txt_trennzeichen = QtWidgets.QLineEdit(ImportCSV)
        self.txt_trennzeichen.setMaxLength(1)
        self.txt_trennzeichen.setObjectName("txt_trennzeichen")
        self.horizontalLayout_3.addWidget(self.txt_trennzeichen)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.line = QtWidgets.QFrame(ImportCSV)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.lbl_EigenschaftKarte = QtWidgets.QLabel(ImportCSV)
        self.lbl_EigenschaftKarte.setObjectName("lbl_EigenschaftKarte")
        self.verticalLayout_3.addWidget(self.lbl_EigenschaftKarte)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.int_spalteWort = QtWidgets.QSpinBox(ImportCSV)
        self.int_spalteWort.setObjectName("int_spalteWort")
        self.horizontalLayout_11.addWidget(self.int_spalteWort)
        self.lbl_muttersprache = QtWidgets.QLabel(ImportCSV)
        self.lbl_muttersprache.setObjectName("lbl_muttersprache")
        self.horizontalLayout_11.addWidget(self.lbl_muttersprache)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.int_spalteFremdwort = QtWidgets.QSpinBox(ImportCSV)
        self.int_spalteFremdwort.setObjectName("int_spalteFremdwort")
        self.horizontalLayout_7.addWidget(self.int_spalteFremdwort)
        self.lbl_Fremdsprache = QtWidgets.QLabel(ImportCSV)
        self.lbl_Fremdsprache.setObjectName("lbl_Fremdsprache")
        self.horizontalLayout_7.addWidget(self.lbl_Fremdsprache)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.int_spalteDefinition = QtWidgets.QSpinBox(ImportCSV)
        self.int_spalteDefinition.setObjectName("int_spalteDefinition")
        self.horizontalLayout_6.addWidget(self.int_spalteDefinition)
        self.lbl_Definition = QtWidgets.QLabel(ImportCSV)
        self.lbl_Definition.setObjectName("lbl_Definition")
        self.horizontalLayout_6.addWidget(self.lbl_Definition)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.int_spalteBemerkung = QtWidgets.QSpinBox(ImportCSV)
        self.int_spalteBemerkung.setObjectName("int_spalteBemerkung")
        self.horizontalLayout_5.addWidget(self.int_spalteBemerkung)
        self.lbl_Bemerkung = QtWidgets.QLabel(ImportCSV)
        self.lbl_Bemerkung.setObjectName("lbl_Bemerkung")
        self.horizontalLayout_5.addWidget(self.lbl_Bemerkung)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9.addLayout(self.verticalLayout)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        spacerItem9 = QtWidgets.QSpacerItem(20, 62, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem9)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_Warnung = QtWidgets.QLabel(ImportCSV)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setItalic(True)
        self.lbl_Warnung.setFont(font)
        self.lbl_Warnung.setStyleSheet("color: rgb(198, 142, 2);")
        self.lbl_Warnung.setObjectName("lbl_Warnung")
        self.horizontalLayout_2.addWidget(self.lbl_Warnung)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.cmd_importieren = QtWidgets.QPushButton(ImportCSV)
        self.cmd_importieren.setObjectName("cmd_importieren")
        self.horizontalLayout_2.addWidget(self.cmd_importieren)
        self.cmd_abbrechen = QtWidgets.QPushButton(ImportCSV)
        self.cmd_abbrechen.setObjectName("cmd_abbrechen")
        self.horizontalLayout_2.addWidget(self.cmd_abbrechen)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ImportCSV)
        QtCore.QMetaObject.connectSlotsByName(ImportCSV)

    def retranslateUi(self, ImportCSV):
        _translate = QtCore.QCoreApplication.translate
        ImportCSV.setWindowTitle(_translate("ImportCSV", "Importieren"))
        self.lbl_Titel.setText(_translate("ImportCSV", "Importieren"))
        self.lbl_name.setText(_translate("ImportCSV", "Name:"))
        self.lbl_sprache.setText(_translate("ImportCSV", "Sprache:"))
        self.cmb_sprache.setItemText(0, _translate("ImportCSV", "Englisch"))
        self.cmb_sprache.setItemText(1, _translate("ImportCSV", "Französisch"))
        self.cmb_sprache.setItemText(2, _translate("ImportCSV", "Latein"))
        self.cmb_sprache.setItemText(3, _translate("ImportCSV", "Spanisch"))
        self.cmb_sprache.setItemText(4, _translate("ImportCSV", "Italienisch"))
        self.lbl_beschreibung.setText(_translate("ImportCSV", "Beschreibung:"))
        self.lbl_pfad.setText(_translate("ImportCSV", "Pfad:"))
        self.cmd_durchsuchen.setText(_translate("ImportCSV", "Durchsuchen"))
        self.lbl_FehlerPfad.setText(_translate("ImportCSV", "Fehler beim Laden der Datei"))
        self.lbl_Vorschau.setText(_translate("ImportCSV", "Vorschau der Datei:"))
        self.lbl_trennzeichen.setText(_translate("ImportCSV", "Trennzeichen:"))
        self.txt_trennzeichen.setText(_translate("ImportCSV", ";"))
        self.lbl_EigenschaftKarte.setText(_translate("ImportCSV", "Spalte in der Importdatei (0 = Nicht vorhanden) | Eigenschaft der Karte"))
        self.lbl_muttersprache.setText(_translate("ImportCSV", "Wort / Ausdruck in der Muttersprache"))
        self.lbl_Fremdsprache.setText(_translate("ImportCSV", "Wort / Ausdruck in der Fremdsprache"))
        self.lbl_Definition.setText(_translate("ImportCSV", "Definition"))
        self.lbl_Bemerkung.setText(_translate("ImportCSV", "Bemerkung"))
        self.lbl_Warnung.setText(_translate("ImportCSV", "Warnung"))
        self.cmd_importieren.setText(_translate("ImportCSV", "Importieren"))
        self.cmd_abbrechen.setText(_translate("ImportCSV", "Abbrechen"))
import ressources_rc
