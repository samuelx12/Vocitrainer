# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hauptfenster.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1066, 749)
        MainWindow.setStyleSheet("selection-background-color: rgb(201, 220, 225);\n"
"selection-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cmd_SetLernen = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_SetLernen.setAutoFillBackground(False)
        self.cmd_SetLernen.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/res/icons/note_stack_FILL1_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.cmd_SetLernen.setIcon(icon)
        self.cmd_SetLernen.setIconSize(QtCore.QSize(30, 30))
        self.cmd_SetLernen.setFlat(False)
        self.cmd_SetLernen.setObjectName("cmd_SetLernen")
        self.horizontalLayout.addWidget(self.cmd_SetLernen)
        self.cmd_SetUeben = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_SetUeben.setAutoFillBackground(False)
        self.cmd_SetUeben.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/icons/model_training_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmd_SetUeben.setIcon(icon1)
        self.cmd_SetUeben.setIconSize(QtCore.QSize(30, 30))
        self.cmd_SetUeben.setFlat(False)
        self.cmd_SetUeben.setObjectName("cmd_SetUeben")
        self.horizontalLayout.addWidget(self.cmd_SetUeben)
        self.cmd_Lernen = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_Lernen.setAutoFillBackground(False)
        self.cmd_Lernen.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/icons/check_box_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/icons/check_box_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.cmd_Lernen.setIcon(icon2)
        self.cmd_Lernen.setIconSize(QtCore.QSize(30, 30))
        self.cmd_Lernen.setFlat(False)
        self.cmd_Lernen.setObjectName("cmd_Lernen")
        self.horizontalLayout.addWidget(self.cmd_Lernen)
        self.cmd_MarkierteLernen = QtWidgets.QPushButton(self.centralwidget)
        self.cmd_MarkierteLernen.setAutoFillBackground(False)
        self.cmd_MarkierteLernen.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/icons/hotel_class_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/icons/hotel_class_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.cmd_MarkierteLernen.setIcon(icon3)
        self.cmd_MarkierteLernen.setIconSize(QtCore.QSize(30, 30))
        self.cmd_MarkierteLernen.setFlat(False)
        self.cmd_MarkierteLernen.setObjectName("cmd_MarkierteLernen")
        self.horizontalLayout.addWidget(self.cmd_MarkierteLernen)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmd_Einstellungen = QtWidgets.QToolButton(self.centralwidget)
        self.cmd_Einstellungen.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/res/icons/settings_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmd_Einstellungen.setIcon(icon4)
        self.cmd_Einstellungen.setIconSize(QtCore.QSize(30, 30))
        self.cmd_Einstellungen.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.cmd_Einstellungen.setObjectName("cmd_Einstellungen")
        self.horizontalLayout.addWidget(self.cmd_Einstellungen)
        self.cmd_Beenden = QtWidgets.QToolButton(self.centralwidget)
        self.cmd_Beenden.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/res/icons/logout_FILL0_wght500_GRAD0_opsz40.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmd_Beenden.setIcon(icon5)
        self.cmd_Beenden.setIconSize(QtCore.QSize(30, 30))
        self.cmd_Beenden.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.cmd_Beenden.setObjectName("cmd_Beenden")
        self.horizontalLayout.addWidget(self.cmd_Beenden)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.line_UnterMenu = QtWidgets.QFrame(self.centralwidget)
        self.line_UnterMenu.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_UnterMenu.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_UnterMenu.setObjectName("line_UnterMenu")
        self.verticalLayout_2.addWidget(self.line_UnterMenu)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.splitter.setFont(font)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.trw_Explorer = QtWidgets.QTreeWidget(self.splitter)
        self.trw_Explorer.setStyleSheet("selection-background-color: rgb(201, 220, 225);\n"
"selection-color: rgb(0, 0, 0);")
        self.trw_Explorer.setObjectName("trw_Explorer")
        self.trw_Explorer.headerItem().setText(0, "1")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tbv_Liste = QtWidgets.QTableView(self.layoutWidget)
        self.tbv_Liste.setStyleSheet("selection-background-color: rgb(201, 220, 225);\n"
"selection-color: rgb(0, 0, 0);")
        self.tbv_Liste.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tbv_Liste.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tbv_Liste.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbv_Liste.setObjectName("tbv_Liste")
        self.tbv_Liste.horizontalHeader().setCascadingSectionResizes(False)
        self.verticalLayout_4.addWidget(self.tbv_Liste)
        self.frame_nichtsAngezeigt = QtWidgets.QFrame(self.layoutWidget)
        self.frame_nichtsAngezeigt.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_nichtsAngezeigt.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_nichtsAngezeigt.setObjectName("frame_nichtsAngezeigt")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_nichtsAngezeigt)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.lbl_nichtsAngezeigt1 = QtWidgets.QLabel(self.frame_nichtsAngezeigt)
        self.lbl_nichtsAngezeigt1.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.lbl_nichtsAngezeigt1.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_nichtsAngezeigt1.setObjectName("lbl_nichtsAngezeigt1")
        self.verticalLayout_5.addWidget(self.lbl_nichtsAngezeigt1)
        self.lbl_nichtsAngezeigt2 = QtWidgets.QLabel(self.frame_nichtsAngezeigt)
        self.lbl_nichtsAngezeigt2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_nichtsAngezeigt2.setWordWrap(True)
        self.lbl_nichtsAngezeigt2.setObjectName("lbl_nichtsAngezeigt2")
        self.verticalLayout_5.addWidget(self.lbl_nichtsAngezeigt2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_4.addWidget(self.frame_nichtsAngezeigt)
        self.verticalLayout_2.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1066, 26))
        self.menubar.setStyleSheet("QMenu: [selection-background-color: rgb(201, 220, 225);\n"
"selection-color: rgb(0, 0, 0);]\n"
"\n"
"QAction: [selection-background-color: rgb(201, 220, 225);\n"
"selection-color: rgb(0, 0, 0);]")
        self.menubar.setObjectName("menubar")
        self.menuVocitrainer = QtWidgets.QMenu(self.menubar)
        self.menuVocitrainer.setObjectName("menuVocitrainer")
        self.menuLernen = QtWidgets.QMenu(self.menubar)
        self.menuLernen.setObjectName("menuLernen")
        self.menuMarketplace = QtWidgets.QMenu(self.menubar)
        self.menuMarketplace.setObjectName("menuMarketplace")
        self.menuImportieren = QtWidgets.QMenu(self.menubar)
        self.menuImportieren.setObjectName("menuImportieren")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.mn_NeuesSet = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/res/icons/note_stack_add_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon6.addPixmap(QtGui.QPixmap(":/icons/res/icons/note_stack_add_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.mn_NeuesSet.setIcon(icon6)
        self.mn_NeuesSet.setObjectName("mn_NeuesSet")
        self.mn_NeuerOrdner = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/res/icons/create_new_folder_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon7.addPixmap(QtGui.QPixmap(":/icons/res/icons/create_new_folder_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.mn_NeuerOrdner.setIcon(icon7)
        self.mn_NeuerOrdner.setObjectName("mn_NeuerOrdner")
        self.mn_Herunterladen = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/res/icons/cloud_download_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon8.addPixmap(QtGui.QPixmap(":/icons/res/icons/cloud_download_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.mn_Herunterladen.setIcon(icon8)
        self.mn_Herunterladen.setObjectName("mn_Herunterladen")
        self.mn_Hochladen = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/res/icons/cloud_upload_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon9.addPixmap(QtGui.QPixmap(":/icons/res/icons/cloud_upload_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.mn_Hochladen.setIcon(icon9)
        self.mn_Hochladen.setObjectName("mn_Hochladen")
        self.mn_HochgeladeneVerwalten = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/res/icons/settings_system_daydream_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon10.addPixmap(QtGui.QPixmap(":/icons/res/icons/settings_system_daydream_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.mn_HochgeladeneVerwalten.setIcon(icon10)
        self.mn_HochgeladeneVerwalten.setObjectName("mn_HochgeladeneVerwalten")
        self.mn_Profil = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/res/icons/manage_accounts_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon11.addPixmap(QtGui.QPixmap(":/icons/res/icons/manage_accounts_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.mn_Profil.setIcon(icon11)
        self.mn_Profil.setObjectName("mn_Profil")
        self.mn_CSV_importieren = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/res/icons/csv_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon12.addPixmap(QtGui.QPixmap(":/icons/res/icons/csv_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.mn_CSV_importieren.setIcon(icon12)
        self.mn_CSV_importieren.setObjectName("mn_CSV_importieren")
        self.mn_Einstellungen = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/res/icons/settings_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon13.addPixmap(QtGui.QPixmap(":/icons/res/icons/settings_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.mn_Einstellungen.setIcon(icon13)
        self.mn_Einstellungen.setObjectName("mn_Einstellungen")
        self.mn_Ueber = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/res/icons/info_FILL0_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon14.addPixmap(QtGui.QPixmap(":/icons/res/icons/info_FILL1_wght400_GRAD0_opsz24.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        self.mn_Ueber.setIcon(icon14)
        self.mn_Ueber.setObjectName("mn_Ueber")
        self.mn_Beenden = QtWidgets.QAction(MainWindow)
        self.mn_Beenden.setIcon(icon5)
        self.mn_Beenden.setObjectName("mn_Beenden")
        self.mn_SetLernen = QtWidgets.QAction(MainWindow)
        self.mn_SetLernen.setIcon(icon)
        self.mn_SetLernen.setObjectName("mn_SetLernen")
        self.mn_SetUeben = QtWidgets.QAction(MainWindow)
        self.mn_SetUeben.setIcon(icon1)
        self.mn_SetUeben.setObjectName("mn_SetUeben")
        self.mn_AusgewaehlteLernen = QtWidgets.QAction(MainWindow)
        self.mn_AusgewaehlteLernen.setIcon(icon2)
        self.mn_AusgewaehlteLernen.setObjectName("mn_AusgewaehlteLernen")
        self.mn_MarkierteLernen = QtWidgets.QAction(MainWindow)
        self.mn_MarkierteLernen.setIcon(icon3)
        self.mn_MarkierteLernen.setObjectName("mn_MarkierteLernen")
        self.menuVocitrainer.addAction(self.mn_NeuesSet)
        self.menuVocitrainer.addAction(self.mn_NeuerOrdner)
        self.menuVocitrainer.addSeparator()
        self.menuVocitrainer.addAction(self.mn_Einstellungen)
        self.menuVocitrainer.addAction(self.mn_Ueber)
        self.menuVocitrainer.addAction(self.mn_Beenden)
        self.menuLernen.addAction(self.mn_SetLernen)
        self.menuLernen.addAction(self.mn_SetUeben)
        self.menuLernen.addSeparator()
        self.menuLernen.addAction(self.mn_AusgewaehlteLernen)
        self.menuLernen.addAction(self.mn_MarkierteLernen)
        self.menuMarketplace.addAction(self.mn_Herunterladen)
        self.menuMarketplace.addAction(self.mn_Hochladen)
        self.menuMarketplace.addAction(self.mn_HochgeladeneVerwalten)
        self.menuMarketplace.addAction(self.mn_Profil)
        self.menuImportieren.addAction(self.mn_CSV_importieren)
        self.menubar.addAction(self.menuVocitrainer.menuAction())
        self.menubar.addAction(self.menuLernen.menuAction())
        self.menubar.addAction(self.menuMarketplace.menuAction())
        self.menubar.addAction(self.menuImportieren.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cmd_SetLernen.setText(_translate("MainWindow", "Set lernen"))
        self.cmd_SetUeben.setText(_translate("MainWindow", "Set üben"))
        self.cmd_Lernen.setText(_translate("MainWindow", "Lernen"))
        self.cmd_MarkierteLernen.setText(_translate("MainWindow", "Markierte lernen"))
        self.cmd_Einstellungen.setText(_translate("MainWindow", "Einstellungen"))
        self.cmd_Beenden.setText(_translate("MainWindow", "Beenden"))
        self.lbl_nichtsAngezeigt1.setText(_translate("MainWindow", "Kein Set ausgewählt."))
        self.lbl_nichtsAngezeigt2.setText(_translate("MainWindow", "Wähle eines links im Explorer aus oder lade dir ein Set vom Server herunter."))
        self.menuVocitrainer.setTitle(_translate("MainWindow", "Vocitrainer"))
        self.menuLernen.setTitle(_translate("MainWindow", "Lernen"))
        self.menuMarketplace.setTitle(_translate("MainWindow", "Marketplace"))
        self.menuImportieren.setTitle(_translate("MainWindow", "Importieren"))
        self.mn_NeuesSet.setText(_translate("MainWindow", "Neues Set"))
        self.mn_NeuerOrdner.setText(_translate("MainWindow", "Neuer Ordner"))
        self.mn_Herunterladen.setText(_translate("MainWindow", "Herunterladen"))
        self.mn_Hochladen.setText(_translate("MainWindow", "Hochladen"))
        self.mn_HochgeladeneVerwalten.setText(_translate("MainWindow", "Hochgeladene verwalten"))
        self.mn_Profil.setText(_translate("MainWindow", "Profil"))
        self.mn_CSV_importieren.setText(_translate("MainWindow", "CSV importieren"))
        self.mn_Einstellungen.setText(_translate("MainWindow", "Einstellungen"))
        self.mn_Ueber.setText(_translate("MainWindow", "Über"))
        self.mn_Beenden.setText(_translate("MainWindow", "Beenden"))
        self.mn_SetLernen.setText(_translate("MainWindow", "Set lernen"))
        self.mn_SetUeben.setText(_translate("MainWindow", "Set üben"))
        self.mn_AusgewaehlteLernen.setText(_translate("MainWindow", "Ausgewählte lernen"))
        self.mn_MarkierteLernen.setText(_translate("MainWindow", "Markierte lernen"))
import ressources_rc
