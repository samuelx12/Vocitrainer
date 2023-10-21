# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mp_logreg.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mpLogReg(object):
    def setupUi(self, mpLogReg):
        mpLogReg.setObjectName("mpLogReg")
        mpLogReg.resize(602, 490)
        mpLogReg.setStyleSheet("QDialog{\n"
"    background-color: rgb(201, 220, 225);\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(mpLogReg)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(mpLogReg)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_log = QtWidgets.QWidget()
        self.page_log.setObjectName("page_log")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.page_log)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(180, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.lbl_login = QtWidgets.QLabel(self.page_log)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lbl_login.setFont(font)
        self.lbl_login.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_login.setObjectName("lbl_login")
        self.verticalLayout_4.addWidget(self.lbl_login)
        self.label_5 = QtWidgets.QLabel(self.page_log)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_log_email = QtWidgets.QLabel(self.page_log)
        self.lbl_log_email.setObjectName("lbl_log_email")
        self.verticalLayout.addWidget(self.lbl_log_email)
        self.txt_log_email = QtWidgets.QLineEdit(self.page_log)
        self.txt_log_email.setObjectName("txt_log_email")
        self.verticalLayout.addWidget(self.txt_log_email)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.label_4 = QtWidgets.QLabel(self.page_log)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_log_passwort = QtWidgets.QLabel(self.page_log)
        self.lbl_log_passwort.setObjectName("lbl_log_passwort")
        self.verticalLayout_2.addWidget(self.lbl_log_passwort)
        self.txt_log_passwort = QtWidgets.QLineEdit(self.page_log)
        self.txt_log_passwort.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_log_passwort.setClearButtonEnabled(False)
        self.txt_log_passwort.setObjectName("txt_log_passwort")
        self.verticalLayout_2.addWidget(self.txt_log_passwort)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.label_6 = QtWidgets.QLabel(self.page_log)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.cmd_zuReg = QtWidgets.QPushButton(self.page_log)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.cmd_zuReg.setFont(font)
        self.cmd_zuReg.setStyleSheet("color: rgb(0, 0, 255);")
        self.cmd_zuReg.setFlat(True)
        self.cmd_zuReg.setObjectName("cmd_zuReg")
        self.horizontalLayout_2.addWidget(self.cmd_zuReg)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.cmd_log = QtWidgets.QPushButton(self.page_log)
        self.cmd_log.setObjectName("cmd_log")
        self.horizontalLayout_3.addWidget(self.cmd_log)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem6)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem7)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        spacerItem8 = QtWidgets.QSpacerItem(179, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.stackedWidget.addWidget(self.page_log)
        self.page_reg = QtWidgets.QWidget()
        self.page_reg.setObjectName("page_reg")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.page_reg)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem9 = QtWidgets.QSpacerItem(158, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem9)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem10)
        self.lbl_registrieren = QtWidgets.QLabel(self.page_reg)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lbl_registrieren.setFont(font)
        self.lbl_registrieren.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_registrieren.setObjectName("lbl_registrieren")
        self.verticalLayout_5.addWidget(self.lbl_registrieren)
        self.label_8 = QtWidgets.QLabel(self.page_reg)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lbl_reg_benutzername = QtWidgets.QLabel(self.page_reg)
        self.lbl_reg_benutzername.setObjectName("lbl_reg_benutzername")
        self.verticalLayout_7.addWidget(self.lbl_reg_benutzername)
        self.txt_reg_benutzername = QtWidgets.QLineEdit(self.page_reg)
        self.txt_reg_benutzername.setObjectName("txt_reg_benutzername")
        self.verticalLayout_7.addWidget(self.txt_reg_benutzername)
        self.label_13 = QtWidgets.QLabel(self.page_reg)
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.verticalLayout_7.addWidget(self.label_13)
        self.lbl_reg_email = QtWidgets.QLabel(self.page_reg)
        self.lbl_reg_email.setObjectName("lbl_reg_email")
        self.verticalLayout_7.addWidget(self.lbl_reg_email)
        self.txt_reg_email = QtWidgets.QLineEdit(self.page_reg)
        self.txt_reg_email.setObjectName("txt_reg_email")
        self.verticalLayout_7.addWidget(self.txt_reg_email)
        self.verticalLayout_6.addLayout(self.verticalLayout_7)
        self.label_10 = QtWidgets.QLabel(self.page_reg)
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_6.addWidget(self.label_10)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.lbl_reg_passwort = QtWidgets.QLabel(self.page_reg)
        self.lbl_reg_passwort.setObjectName("lbl_reg_passwort")
        self.verticalLayout_8.addWidget(self.lbl_reg_passwort)
        self.txt_reg_passwort = QtWidgets.QLineEdit(self.page_reg)
        self.txt_reg_passwort.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_reg_passwort.setClearButtonEnabled(False)
        self.txt_reg_passwort.setObjectName("txt_reg_passwort")
        self.verticalLayout_8.addWidget(self.txt_reg_passwort)
        self.verticalLayout_6.addLayout(self.verticalLayout_8)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.label_12 = QtWidgets.QLabel(self.page_reg)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.verticalLayout_5.addWidget(self.label_12)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem11)
        self.cmd_zuLog = QtWidgets.QPushButton(self.page_reg)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.cmd_zuLog.setFont(font)
        self.cmd_zuLog.setStyleSheet("color: rgb(0, 0, 255);")
        self.cmd_zuLog.setFlat(True)
        self.cmd_zuLog.setObjectName("cmd_zuLog")
        self.horizontalLayout_5.addWidget(self.cmd_zuLog)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem12)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem13)
        self.cmd_reg = QtWidgets.QPushButton(self.page_reg)
        self.cmd_reg.setObjectName("cmd_reg")
        self.horizontalLayout_6.addWidget(self.cmd_reg)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem14)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem15)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem16)
        self.horizontalLayout_7.addLayout(self.verticalLayout_5)
        spacerItem17 = QtWidgets.QSpacerItem(157, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem17)
        self.stackedWidget.addWidget(self.page_reg)
        self.horizontalLayout.addWidget(self.stackedWidget)

        self.retranslateUi(mpLogReg)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mpLogReg)

    def retranslateUi(self, mpLogReg):
        _translate = QtCore.QCoreApplication.translate
        mpLogReg.setWindowTitle(_translate("mpLogReg", "Dialog"))
        self.lbl_login.setText(_translate("mpLogReg", "Login"))
        self.lbl_log_email.setText(_translate("mpLogReg", "E-Mail"))
        self.lbl_log_passwort.setText(_translate("mpLogReg", "Passwort"))
        self.cmd_zuReg.setText(_translate("mpLogReg", "Noch kein Konto?"))
        self.cmd_log.setText(_translate("mpLogReg", "Login"))
        self.lbl_registrieren.setText(_translate("mpLogReg", "Registrieren"))
        self.lbl_reg_benutzername.setText(_translate("mpLogReg", "Benutzername (öffentlich sichtbar)"))
        self.lbl_reg_email.setText(_translate("mpLogReg", "E-Mail"))
        self.lbl_reg_passwort.setText(_translate("mpLogReg", "Passwort"))
        self.cmd_zuLog.setText(_translate("mpLogReg", "Du hast bereits ein Konto?"))
        self.cmd_reg.setText(_translate("mpLogReg", "Registrieren"))
