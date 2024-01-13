# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ueber.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Ueber(object):
    def setupUi(self, Ueber):
        Ueber.setObjectName("Ueber")
        Ueber.resize(447, 424)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/icons/info_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Ueber.setWindowIcon(icon)
        Ueber.setModal(False)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Ueber)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_6 = QtWidgets.QLabel(Ueber)
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap(":/icons/res/icons/Vocitrainer_Icon.svg"))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_vocitrainer = QtWidgets.QLabel(Ueber)
        self.lbl_vocitrainer.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";")
        self.lbl_vocitrainer.setObjectName("lbl_vocitrainer")
        self.verticalLayout.addWidget(self.lbl_vocitrainer)
        self.lbl_text = QtWidgets.QLabel(Ueber)
        self.lbl_text.setWordWrap(True)
        self.lbl_text.setObjectName("lbl_text")
        self.verticalLayout.addWidget(self.lbl_text)
        self.lbl_version_vocitrainer = QtWidgets.QLabel(Ueber)
        self.lbl_version_vocitrainer.setTextFormat(QtCore.Qt.RichText)
        self.lbl_version_vocitrainer.setWordWrap(True)
        self.lbl_version_vocitrainer.setObjectName("lbl_version_vocitrainer")
        self.verticalLayout.addWidget(self.lbl_version_vocitrainer)
        self.lbl_version_qt = QtWidgets.QLabel(Ueber)
        self.lbl_version_qt.setObjectName("lbl_version_qt")
        self.verticalLayout.addWidget(self.lbl_version_qt)
        self.lbl_version_pyqt = QtWidgets.QLabel(Ueber)
        self.lbl_version_pyqt.setObjectName("lbl_version_pyqt")
        self.verticalLayout.addWidget(self.lbl_version_pyqt)
        self.label = QtWidgets.QLabel(Ueber)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.cmd_Schliessen = QtWidgets.QPushButton(Ueber)
        self.cmd_Schliessen.setObjectName("cmd_Schliessen")
        self.horizontalLayout.addWidget(self.cmd_Schliessen)
        spacerItem4 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Ueber)
        QtCore.QMetaObject.connectSlotsByName(Ueber)

    def retranslateUi(self, Ueber):
        _translate = QtCore.QCoreApplication.translate
        Ueber.setWindowTitle(_translate("Ueber", "Über Vocitrainer"))
        self.lbl_vocitrainer.setText(_translate("Ueber", "Vocitrainer"))
        self.lbl_text.setText(_translate("Ueber", "Vocitrainer ist ein Projekt von Samuel Barmet, umgesetzt im Rahmen der Maturaarbeit."))
        self.lbl_version_vocitrainer.setText(_translate("Ueber", "Vocitrainer: 1.0"))
        self.lbl_version_qt.setText(_translate("Ueber", "Qt: "))
        self.lbl_version_pyqt.setText(_translate("Ueber", "PyQt:"))
        self.label.setText(_translate("Ueber", "Icons von Google Fonts."))
        self.cmd_Schliessen.setText(_translate("Ueber", "Schliessen"))
import ressources_rc
