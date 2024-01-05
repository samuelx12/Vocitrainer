# -*- coding: utf-8 -*-
"""
explorer_item.py
Hier ist die Klasse ExplorerItem enthalten die für den Explorer im Hauptfenster benötigt wird.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ExplorerItem(QTreeWidgetItem):
    """
    Das Explorer Item ist eine Zeile in der Übersicht der Lernsets, die rechts angezeigt wird.
    """

    def __init__(self, txt, typ, id, parent: QTreeWidgetItem = None):
        """
        @param txt: Der Text den das Item zeigt
        """
        super().__init__(parent)
        self.setText(0, txt)
        icon = QIcon()
        self.id = id
        self.typ = typ
        self.txt = txt
        if typ == "ordner":
            icon.addPixmap(QPixmap("res/icons/folder_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
            icon.addPixmap(QPixmap("res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.On)
        elif typ == "vociset":
            icon.addPixmap(QPixmap("res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)

        self.setIcon(0, icon)

        # Das Item dem übergestellten Item zuordnen, falls dieses bekannt
        if parent:
            parent.addChild(self)

    def setActive(self, aktiv: bool) -> None:
        """Führt eine änderung des Icons durch je nach Status"""
        icon = QIcon()

        # Dicke Schrift an bzw. aus machen
        if self.typ == "vociset":
            font = QFont()
            font.setBold(aktiv)
            self.setFont(0, font)

        if aktiv:
            if self.typ == "vociset":
                icon.addPixmap(QPixmap("res/icons/note_stack_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Normal,
                               QIcon.Off)
            elif self.typ == "ordner":
                icon.addPixmap(QPixmap("res/icons/folder_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
                icon.addPixmap(QPixmap("res/icons/folder_open_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Normal,
                               QIcon.On)
        else:
            if self.typ == "vociset":
                icon.addPixmap(QPixmap("res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal,
                               QIcon.Off)
            elif self.typ == "ordner":
                icon.addPixmap(QPixmap("res/icons/folder_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
                icon.addPixmap(QPixmap("res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.On)

        self.setIcon(0, icon)
