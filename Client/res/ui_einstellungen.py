# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'einstellungen.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Einstellungen(object):
    def setupUi(self, Einstellungen):
        Einstellungen.setObjectName("Einstellungen")
        Einstellungen.resize(695, 749)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/icons/settings_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Einstellungen.setWindowIcon(icon)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Einstellungen)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(Einstellungen)
        self.label_3.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.frame = QtWidgets.QFrame(Einstellungen)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap(":/icons/res/icons/settings_FILL0_wght400_GRAD0_opsz24.svg"))
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_7.addWidget(self.label_12)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout_7.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.cmb_stil = QtWidgets.QComboBox(self.frame)
        self.cmb_stil.setObjectName("cmb_stil")
        self.cmb_stil.addItem("")
        self.cmb_stil.addItem("")
        self.horizontalLayout.addWidget(self.cmb_stil)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.frame_willkommenEinstellungen = QtWidgets.QFrame(self.frame)
        self.frame_willkommenEinstellungen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_willkommenEinstellungen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_willkommenEinstellungen.setObjectName("frame_willkommenEinstellungen")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_willkommenEinstellungen)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.box_willkommenMeldung = QtWidgets.QCheckBox(self.frame_willkommenEinstellungen)
        self.box_willkommenMeldung.setObjectName("box_willkommenMeldung")
        self.horizontalLayout_11.addWidget(self.box_willkommenMeldung)
        self.cmd_anzeigen = QtWidgets.QPushButton(self.frame_willkommenEinstellungen)
        self.cmd_anzeigen.setObjectName("cmd_anzeigen")
        self.horizontalLayout_11.addWidget(self.cmd_anzeigen)
        spacerItem2 = QtWidgets.QSpacerItem(272, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.frame_willkommenEinstellungen)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.cmb_sprache = QtWidgets.QComboBox(self.frame)
        self.cmb_sprache.setObjectName("cmb_sprache")
        self.cmb_sprache.addItem("")
        self.cmb_sprache.addItem("")
        self.cmb_sprache.addItem("")
        self.cmb_sprache.addItem("")
        self.cmb_sprache.addItem("")
        self.horizontalLayout_4.addWidget(self.cmb_sprache)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Einstellungen)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_13 = QtWidgets.QLabel(self.frame_2)
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap(":/icons/res/icons/note_stack_FILL0_wght400_GRAD0_opsz24.svg"))
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_9.addWidget(self.label_13)
        self.label_14 = QtWidgets.QLabel(self.frame_2)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_9.addWidget(self.label_14)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.cmb_mz = QtWidgets.QComboBox(self.frame_2)
        self.cmb_mz.setObjectName("cmb_mz")
        self.cmb_mz.addItem("")
        self.cmb_mz.addItem("")
        self.cmb_mz.addItem("")
        self.cmb_mz.addItem("")
        self.cmb_mz.addItem("")
        self.horizontalLayout_3.addWidget(self.cmb_mz)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.cmb_ft = QtWidgets.QComboBox(self.frame_2)
        self.cmb_ft.setObjectName("cmb_ft")
        self.cmb_ft.addItem("")
        self.cmb_ft.addItem("")
        self.cmb_ft.addItem("")
        self.horizontalLayout_2.addWidget(self.cmb_ft)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.box_definitionLernen = QtWidgets.QCheckBox(self.frame_2)
        self.box_definitionLernen.setObjectName("box_definitionLernen")
        self.verticalLayout_2.addWidget(self.box_definitionLernen)
        self.box_fokusmodus = QtWidgets.QCheckBox(self.frame_2)
        self.box_fokusmodus.setObjectName("box_fokusmodus")
        self.verticalLayout_2.addWidget(self.box_fokusmodus)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(Einstellungen)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setText("")
        self.label_15.setPixmap(QtGui.QPixmap(":/icons/res/icons/manage_accounts_FILL0_wght400_GRAD0_opsz24.svg"))
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_10.addWidget(self.label_15)
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_10.addWidget(self.label_16)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lbl_profilStatus = QtWidgets.QLabel(self.frame_3)
        self.lbl_profilStatus.setObjectName("lbl_profilStatus")
        self.horizontalLayout_5.addWidget(self.lbl_profilStatus)
        self.cmd_xxMelden = QtWidgets.QPushButton(self.frame_3)
        self.cmd_xxMelden.setObjectName("cmd_xxMelden")
        self.horizontalLayout_5.addWidget(self.cmd_xxMelden)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.lbl_email = QtWidgets.QLabel(self.frame_3)
        self.lbl_email.setObjectName("lbl_email")
        self.verticalLayout_3.addWidget(self.lbl_email)
        self.lbl_benutzername = QtWidgets.QLabel(self.frame_3)
        self.lbl_benutzername.setObjectName("lbl_benutzername")
        self.verticalLayout_3.addWidget(self.lbl_benutzername)
        self.lbl_passwort = QtWidgets.QLabel(self.frame_3)
        self.lbl_passwort.setObjectName("lbl_passwort")
        self.verticalLayout_3.addWidget(self.lbl_passwort)
        self.verticalLayout_4.addWidget(self.frame_3)
        spacerItem9 = QtWidgets.QSpacerItem(20, 205, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem9)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem10)
        self.cmd_ok = QtWidgets.QPushButton(Einstellungen)
        self.cmd_ok.setDefault(True)
        self.cmd_ok.setObjectName("cmd_ok")
        self.horizontalLayout_6.addWidget(self.cmd_ok)
        self.cmd_abbrechen = QtWidgets.QPushButton(Einstellungen)
        self.cmd_abbrechen.setObjectName("cmd_abbrechen")
        self.horizontalLayout_6.addWidget(self.cmd_abbrechen)
        self.cmd_uebernehmen = QtWidgets.QPushButton(Einstellungen)
        self.cmd_uebernehmen.setObjectName("cmd_uebernehmen")
        self.horizontalLayout_6.addWidget(self.cmd_uebernehmen)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.retranslateUi(Einstellungen)
        QtCore.QMetaObject.connectSlotsByName(Einstellungen)

    def retranslateUi(self, Einstellungen):
        _translate = QtCore.QCoreApplication.translate
        Einstellungen.setWindowTitle(_translate("Einstellungen", "Einstellungen"))
        self.label_3.setText(_translate("Einstellungen", "Einstellungen"))
        self.label.setText(_translate("Einstellungen", "Allgemein"))
        self.label_2.setText(_translate("Einstellungen", "Stil (Neustart erforderlich):"))
        self.cmb_stil.setItemText(0, _translate("Einstellungen", "Vocitrainer"))
        self.cmb_stil.setItemText(1, _translate("Einstellungen", "Windows"))
        self.box_willkommenMeldung.setText(_translate("Einstellungen", "Willkommen-Meldung zum Start anzeigen"))
        self.cmd_anzeigen.setText(_translate("Einstellungen", "Anzeigen"))
        self.label_7.setText(_translate("Einstellungen", "Standartsprache für neues Set:"))
        self.cmb_sprache.setItemText(0, _translate("Einstellungen", "Englisch"))
        self.cmb_sprache.setItemText(1, _translate("Einstellungen", "Französisch"))
        self.cmb_sprache.setItemText(2, _translate("Einstellungen", "Latein"))
        self.cmb_sprache.setItemText(3, _translate("Einstellungen", "Spanisch"))
        self.cmb_sprache.setItemText(4, _translate("Einstellungen", "Italienisch"))
        self.label_14.setText(_translate("Einstellungen", "Intelligenter Lernmodus (\"Set lernen\")"))
        self.label_6.setText(_translate("Einstellungen", "Millersche Zahl"))
        self.cmb_mz.setItemText(0, _translate("Einstellungen", "5"))
        self.cmb_mz.setItemText(1, _translate("Einstellungen", "6"))
        self.cmb_mz.setItemText(2, _translate("Einstellungen", "7 - Normal"))
        self.cmb_mz.setItemText(3, _translate("Einstellungen", "8"))
        self.cmb_mz.setItemText(4, _translate("Einstellungen", "9"))
        self.label_5.setText(_translate("Einstellungen", "Fehlertoleranz:"))
        self.cmb_ft.setItemText(0, _translate("Einstellungen", "Tief"))
        self.cmb_ft.setItemText(1, _translate("Einstellungen", "Normal"))
        self.cmb_ft.setItemText(2, _translate("Einstellungen", "Hoch"))
        self.box_definitionLernen.setText(_translate("Einstellungen", "Definition lernen"))
        self.box_fokusmodus.setText(_translate("Einstellungen", "Erhöhter Fokus"))
        self.label_16.setText(_translate("Einstellungen", "Profil (Marketplace)"))
        self.lbl_profilStatus.setText(_translate("Einstellungen", "Angemeldet / Abgemeldet"))
        self.cmd_xxMelden.setText(_translate("Einstellungen", "Abmelden"))
        self.lbl_email.setText(_translate("Einstellungen", "E-Mail"))
        self.lbl_benutzername.setText(_translate("Einstellungen", "Benutzername"))
        self.lbl_passwort.setText(_translate("Einstellungen", "Passwort"))
        self.cmd_ok.setText(_translate("Einstellungen", "Ok"))
        self.cmd_abbrechen.setText(_translate("Einstellungen", "Abbrechen"))
        self.cmd_uebernehmen.setText(_translate("Einstellungen", "Übernehmen"))
import ressources_rc
