# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Hauptfenster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Vocitrainer")

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(651, 561)
        self.mn_Ueber = QAction(MainWindow)
        self.mn_Ueber.setObjectName(u"mn_Ueber")
        self.mn_NeuesSet = QAction(MainWindow)
        self.mn_NeuesSet.setObjectName(u"mn_NeuesSet")
        self.mn_NeuerOrdner = QAction(MainWindow)
        self.mn_NeuerOrdner.setObjectName(u"mn_NeuerOrdner")
        self.mn_Einstellungen = QAction(MainWindow)
        self.mn_Einstellungen.setObjectName(u"mn_Einstellungen")
        self.mn_Einstellungen.setCheckable(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_SetLernen = QPushButton(self.centralwidget)
        self.pb_SetLernen.setObjectName(u"pb_SetLernen")

        self.horizontalLayout.addWidget(self.pb_SetLernen)

        self.pb_AusgewaehlteLernen = QPushButton(self.centralwidget)
        self.pb_AusgewaehlteLernen.setObjectName(u"pb_AusgewaehlteLernen")

        self.horizontalLayout.addWidget(self.pb_AusgewaehlteLernen)

        self.hs_Menu = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.hs_Menu)

        self.pb_Beenden = QPushButton(self.centralwidget)
        self.pb_Beenden.setObjectName(u"pb_Beenden")

        self.horizontalLayout.addWidget(self.pb_Beenden)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line_UnterMenu = QFrame(self.centralwidget)
        self.line_UnterMenu.setObjectName(u"line_UnterMenu")
        self.line_UnterMenu.setFrameShape(QFrame.HLine)
        self.line_UnterMenu.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_UnterMenu)

        self.splitter_ExplorerListe = QSplitter(self.centralwidget)
        self.splitter_ExplorerListe.setObjectName(u"splitter_ExplorerListe")
        self.splitter_ExplorerListe.setMaximumSize(QSize(16777215, 16777215))
        self.splitter_ExplorerListe.setOrientation(Qt.Horizontal)
        self.splitter_ExplorerListe.setOpaqueResize(True)
        self.splitter_ExplorerListe.setHandleWidth(7)
        self.splitter_ExplorerListe.setChildrenCollapsible(True)
        self.trv_Explorer = QTreeView(self.splitter_ExplorerListe)
        self.trv_Explorer.setObjectName(u"trv_Explorer")
        self.splitter_ExplorerListe.addWidget(self.trv_Explorer)
        self.tbv_Liste = QColumnView(self.splitter_ExplorerListe)
        self.tbv_Liste.setObjectName(u"tbv_Liste")
        self.splitter_ExplorerListe.addWidget(self.tbv_Liste)

        self.verticalLayout.addWidget(self.splitter_ExplorerListe)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 651, 22))
        self.menuVocitrainer = QMenu(self.menubar)
        self.menuVocitrainer.setObjectName(u"menuVocitrainer")
        self.menuLernen = QMenu(self.menubar)
        self.menuLernen.setObjectName(u"menuLernen")
        self.menu_Extra = QMenu(self.menubar)
        self.menu_Extra.setObjectName(u"menu_Extra")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuVocitrainer.menuAction())
        self.menubar.addAction(self.menuLernen.menuAction())
        self.menubar.addAction(self.menu_Extra.menuAction())
        self.menuVocitrainer.addAction(self.mn_NeuesSet)
        self.menuVocitrainer.addAction(self.mn_NeuerOrdner)
        self.menuVocitrainer.addSeparator()
        self.menu_Extra.addAction(self.mn_Einstellungen)
        self.menu_Extra.addAction(self.mn_Ueber)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.mn_Ueber.setText(QCoreApplication.translate("MainWindow", u"\u00dcber", None))
        self.mn_NeuesSet.setText(QCoreApplication.translate("MainWindow", u"Neues Set", None))
        self.mn_NeuerOrdner.setText(QCoreApplication.translate("MainWindow", u"Neuer Ordner", None))
        self.mn_Einstellungen.setText(QCoreApplication.translate("MainWindow", u"Einstellungen", None))
        # if QT_CONFIG(tooltip)
        self.pb_SetLernen.setToolTip(QCoreApplication.translate("MainWindow", u"Dieses Set lernen", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.pb_SetLernen.setStatusTip(QCoreApplication.translate("MainWindow", u"Jetzt lernen", None))
        # endif // QT_CONFIG(statustip)
        self.pb_SetLernen.setText(QCoreApplication.translate("MainWindow", u"Set lernen", None))
        self.pb_AusgewaehlteLernen.setText(QCoreApplication.translate("MainWindow", u"Ausgew\u00e4hlte lernen", None))
        self.pb_Beenden.setText(QCoreApplication.translate("MainWindow", u"Beenden", None))
        self.menuVocitrainer.setTitle(QCoreApplication.translate("MainWindow", u"Vocitrainer", None))
        self.menuLernen.setTitle(QCoreApplication.translate("MainWindow", u"Lernen", None))
        self.menu_Extra.setTitle(QCoreApplication.translate("MainWindow", u"Extra", None))
    # retranslateUi
