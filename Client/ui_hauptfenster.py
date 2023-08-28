# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hauptfenster.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(641, 543)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cmd_SetLernen = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_SetLernen.setObjectName("cmd_SetLernen")
        self.horizontalLayout_2.addWidget(self.cmd_SetLernen)
        self.cmd_AusgewaehlteLernen = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_AusgewaehlteLernen.setObjectName("cmd_AusgewaehlteLernen")
        self.horizontalLayout_2.addWidget(self.cmd_AusgewaehlteLernen)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cmd_Beenden = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_Beenden.setObjectName("cmd_Beenden")
        self.horizontalLayout_2.addWidget(self.cmd_Beenden)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_UnterMenu = QtWidgets.QFrame(self.centralwidget)
        self.line_UnterMenu.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_UnterMenu.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_UnterMenu.setObjectName("line_UnterMenu")
        self.verticalLayout.addWidget(self.line_UnterMenu)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.trw_Explorer = QtWidgets.QTreeWidget(self.splitter)
        self.trw_Explorer.setStyleSheet("selection-background-color: rgb(201, 220, 225);\n"
"selection-color: rgb(0, 0, 0);")
        self.trw_Explorer.setObjectName("trw_Explorer")
        item_0 = QtWidgets.QTreeWidgetItem(self.trw_Explorer)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/icons/folder_FILL0_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap("res/icons/folder_FILL1_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("res/icons/folder_open_FILL1_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        item_0.setIcon(0, icon)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("res/icons/note_stack_FILL1_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        item_1.setIcon(0, icon1)
        self.tbv_Liste = QtWidgets.QTableView(self.splitter)
        self.tbv_Liste.setObjectName("tbv_Liste")
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 641, 22))
        self.menubar.setObjectName("menubar")
        self.menuVocitrainer = QtWidgets.QMenu(self.menubar)
        self.menuVocitrainer.setObjectName("menuVocitrainer")
        self.menuLernen = QtWidgets.QMenu(self.menubar)
        self.menuLernen.setObjectName("menuLernen")
        self.menu_Extra = QtWidgets.QMenu(self.menubar)
        self.menu_Extra.setObjectName("menu_Extra")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.mn_Ueber = QtWidgets.QAction(MainWindow)
        self.mn_Ueber.setObjectName("mn_Ueber")
        self.mn_NeuesSet = QtWidgets.QAction(MainWindow)
        self.mn_NeuesSet.setObjectName("mn_NeuesSet")
        self.mn_NeuerOrdner = QtWidgets.QAction(MainWindow)
        self.mn_NeuerOrdner.setObjectName("mn_NeuerOrdner")
        self.mn_Einstellungen = QtWidgets.QAction(MainWindow)
        self.mn_Einstellungen.setCheckable(False)
        self.mn_Einstellungen.setObjectName("mn_Einstellungen")
        self.menuVocitrainer.addAction(self.mn_NeuesSet)
        self.menuVocitrainer.addAction(self.mn_NeuerOrdner)
        self.menuVocitrainer.addSeparator()
        self.menu_Extra.addAction(self.mn_Einstellungen)
        self.menu_Extra.addAction(self.mn_Ueber)
        self.menubar.addAction(self.menuVocitrainer.menuAction())
        self.menubar.addAction(self.menuLernen.menuAction())
        self.menubar.addAction(self.menu_Extra.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cmd_SetLernen.setToolTip(_translate("MainWindow", "Dieses Set lernen"))
        self.cmd_SetLernen.setStatusTip(_translate("MainWindow", "Jetzt lernen"))
        self.cmd_SetLernen.setText(_translate("MainWindow", "Set lernen"))
        self.cmd_AusgewaehlteLernen.setText(_translate("MainWindow", "Ausgewählte lernen"))
        self.cmd_Beenden.setText(_translate("MainWindow", "Beenden"))
        self.trw_Explorer.headerItem().setText(0, _translate("MainWindow", "1"))
        __sortingEnabled = self.trw_Explorer.isSortingEnabled()
        self.trw_Explorer.setSortingEnabled(False)
        self.trw_Explorer.topLevelItem(0).setText(0, _translate("MainWindow", "ELEMENT"))
        self.trw_Explorer.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "Unterelement"))
        self.trw_Explorer.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "Vociset"))
        self.trw_Explorer.setSortingEnabled(__sortingEnabled)
        self.menuVocitrainer.setTitle(_translate("MainWindow", "Vocitrainer"))
        self.menuLernen.setTitle(_translate("MainWindow", "Lernen"))
        self.menu_Extra.setTitle(_translate("MainWindow", "Extra"))
        self.mn_Ueber.setText(_translate("MainWindow", "Über"))
        self.mn_NeuesSet.setText(_translate("MainWindow", "Neues Set"))
        self.mn_NeuerOrdner.setText(_translate("MainWindow", "Neuer Ordner"))
        self.mn_Einstellungen.setText(_translate("MainWindow", "Einstellungen"))
