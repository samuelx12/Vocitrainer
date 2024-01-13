# -*- coding: utf-8 -*-
"""
explorer_item.py
Hier ist die Klasse ExplorerItem enthalten die für den Explorer im Hauptfenster benötigt wird.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from rich import print as rprint


class ExplorerItem(QTreeWidgetItem):
    """
    Das Explorer Item ist eine Zeile in der Übersicht der Lernsets, die rechts angezeigt wird.
    """

    def __init__(
            self,
            txt: str,
            typ: str,
            id: int,
            parent: QTreeWidgetItem = None,
            sprache: str = "Fremdsprache",
            beschreibung: str = ""
    ):
        """
        @param txt: Der Text den das Item zeigt
        """
        super().__init__(parent)
        self.setText(0, txt)
        icon = QIcon()
        self.id = id
        self.typ = typ
        self.txt = txt
        self.sprache = sprache
        self.beschreibung = beschreibung

        if typ == "ordner":
            icon.addPixmap(
                QPixmap(":/icons/res/icons/folder_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
            icon.addPixmap(
                QPixmap(":/icons/res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.On)
        elif typ == "vociset":
            icon.addPixmap(
                QPixmap(":/icons/res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)

            if beschreibung == "":
                tooltip = (
                        f"Sprache: {sprache}\n" +
                        "Beschreibung: (leer)"
                )
            else:
                tooltip = (
                        f"Sprache: {sprache}\n" +
                        "Beschreibung:\n" +
                        beschreibung
                )
            self.setToolTip(0, tooltip)

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
            try:
                self.setFont(0, font)
            except RuntimeError:
                pass
                # rprint(
                #     """[yellow]INFO Der "[italic]wrapped C/C++ object of type ExplorerItem has been""" +
                #     """deleted[/italic]"-Runtime Error wurde gerade abgefangen.""" +
                #     """ [green]Diese Nachricht kann ignoriert werden, obwohl sie mehrmals hintereinander auftritt."""
                # )

        if aktiv:
            if self.typ == "vociset":
                icon.addPixmap(QPixmap(":/icons/res/icons/note_stack_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Normal,
                               QIcon.Off)
            elif self.typ == "ordner":
                icon.addPixmap(QPixmap(":/icons/res/icons/folder_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
                icon.addPixmap(QPixmap(":/icons/res/icons/folder_open_FILL1_wght500_GRAD0_opsz40.svg"), QIcon.Normal,
                               QIcon.On)
        else:
            if self.typ == "vociset":
                icon.addPixmap(QPixmap(":/icons/res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal,
                               QIcon.Off)
            elif self.typ == "ordner":
                icon.addPixmap(QPixmap(":/icons/res/icons/folder_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.Off)
                icon.addPixmap(QPixmap(":/icons/res/icons/folder_open_FILL0_wght500_GRAD0_opsz40.svg"), QIcon.Normal, QIcon.On)

        try:
            self.setIcon(0, icon)
        except RuntimeError:
            pass
            # rprint(
            #     """[yellow]INFO Der "[italic]wrapped C/C++ object of type ExplorerItem has been""" +
            #     """deleted[/italic]"-Runtime Error wurde gerade abgefangen.""" +
            #     """ [green]Diese Nachricht kann ignoriert werden, obwohl sie mehrmals hintereinander auftritt."""
            # )

    def tooltip_neuladen(self):
        """ToolTip neuladen"""
        if self.beschreibung == "":
            tooltip = (
                    f"Sprache: {self.sprache}\n" +
                    "Beschreibung: (leer)"
            )
        else:
            tooltip = (
                    f"Sprache: {self.sprache}\n" +
                    "Beschreibung:\n" +
                    self.beschreibung
            )

        self.setToolTip(0, tooltip)

    def set_name(self, name: str):
        """Setter für den Namen."""
        self.txt = name
        self.setText(0, self.txt)

    def set_sprache(self, sprache: str):
        """Setter für die Sprache."""
        self.sprache = sprache
        self.tooltip_neuladen()

    def set_beschreibung(self, beschreibung: str):
        """Setter für die Beschreibung."""
        self.beschreibung = beschreibung
        self.tooltip_neuladen()
