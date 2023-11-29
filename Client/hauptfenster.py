# -*- coding: utf-8 -*-
"""
hauptfenster.py
Diese Datei enthält eigentlich nur die Klasse Hauptfenster, welche von QMainWindow erbt. Das Hauptfenster ist das erste
Fenster, welches aufgeht. Das Programm läuft weiter, wenn Signale auftreten, welche mit einem Slot (Funktion) verbunden
wurden (Qt-Konzept)
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from models import KartenModel
from explorer_item import ExplorerItem
import sqlite3
from Client.res.qt.ui_hauptfenster import Ui_MainWindow
from trainingsfenster import Trainingsfenster
from Mp_herunterladen import MpHerunterladen
from Mp_Hochladen import MpHochladen
from importCSV import ImportCSV
from typing import List
from Mp_LogReg import log_reg


class Hauptfenster(QMainWindow, Ui_MainWindow):
    """
    Diese Klasse repräsentiert das Hauptfenster. Sie erbt das Aussehen von der vom Qt-Designer exportierten Klasse.
    Dieses befindet sich in einer eigenen Datei, was den Workflow erheblich erleichtert, weil gleich die ganze
    Datei ohne Gefahr neu überschrieben werden kann.
    """

    def __init__(self, *args, obj=None, **kwargs):
        super(Hauptfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Vocitrainer")
        self.setWindowIcon(QIcon("res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"))

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite/6), int(hoehe/6), int(breite*2/3), int(hoehe*2/3))
        # Splitter richtig einteilen
        self.splitter.setSizes([100, 300])
        self.splitter.updateGeometry()

        # Tabellen Model erstellen und zuweisen
        self.conn = sqlite3.connect('vocitrainerdb.db')
        print("Datenbankverbindung wurde erstellt")
        self.kartenModel = KartenModel(dbconn=self.conn)
        print("Model wurde erstellt")

        # Tabellen Model Daten laden
        self.kartenModel.lade_daten(1)
        self.geladenes_set_explorer_item = None

        # Model zuweisen
        self.tbv_Liste.setModel(self.kartenModel)
        print("Model wurde zugewiesen")
        self.tbv_Liste.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tbv_Liste.horizontalHeader().setStretchLastSection(True)

        # Explorer vorbereiten
        self.rootNode = self.trw_Explorer.invisibleRootItem()
        self.load_explorer()
        self.trw_Explorer.setDragEnabled(True)
        self.trw_Explorer.setAcceptDrops(True)
        self.trw_Explorer.setDropIndicatorShown(True)
        self.trw_Explorer.setDefaultDropAction(Qt.MoveAction)
        self.trw_Explorer.setSelectionMode(QTreeWidget.ExtendedSelection)

        # Signals und Slots verbinden
        self.cmd_Beenden.clicked.connect(self.cmd_beenden_clicked)
        self.cmd_SetLernen.clicked.connect(self.cmd_Setlernen_clicked)
        self.trw_Explorer.doubleClicked.connect(self.trw_Explorer_doubleClicked)
        self.trw_Explorer.dragEnterEvent = self.trw_Explorer_dragEnterEvent
        self.trw_Explorer.dropEvent = self.trw_Explorer_dropEvent
        # Menu
        self.mn_Herunterladen.triggered.connect(self.mn_Herunterladen_triggered)
        self.mn_CSV_importieren.triggered.connect(self.mn_CSV_importieren_triggered)
        self.mn_Hochladen.triggered.connect(self.mn_Hochladen_triggered)

        # Kontextmenüs aktivieren
        self.trw_Explorer.setContextMenuPolicy(Qt.CustomContextMenu)
        self.trw_Explorer.customContextMenuRequested.connect(self.trw_Explorer_Kontextmenu)

        # Aktives Element im Explorer speichern
        self.aktiveItems = []

    def cmd_beenden_clicked(self):
        self.close()

    def cmd_Setlernen_clicked(self):
        self.trainingsfenster = Trainingsfenster()
        self.trainingsfenster.setModal(True)

        self.trainingsfenster.exec_()

    def load_explorer(self):
        def ebene_laden(parent, parent_id):
            """Diese Funktion ladet Rekursiv die Ordnerstruktur"""
            # Ordner dieser Ebene laden
            query = "SELECT ordner_id, ordner_name, farbe, urordner_id FROM ordner WHERE urordner_id = ?"
            lade_cursor.execute(query, (parent_id,))
            result = lade_cursor.fetchall()

            # Resultat in Liste umwandeln
            ordner = []
            for reihe in result:
                ordner.append(reihe)

            # Vocisets dieser Ebene laden
            query = "SELECT set_id, set_name, beschreibung, sprache FROM vociset WHERE urordner_id = ?"
            lade_cursor.execute(query, (parent_id,))
            print(parent_id)
            result = lade_cursor.fetchall()

            # Resultat in Liste umwandeln
            vocisets = []
            for reihe in result:
                vocisets.append(reihe)

            for i_ordner in ordner:
                neuer_ordner = ExplorerItem(i_ordner[1], "ordner", i_ordner[0], parent=parent)
                ebene_laden(neuer_ordner, i_ordner[0])

            for i_vociset in vocisets:
                neues_vociset = ExplorerItem(i_vociset[1], "vociset", i_vociset[0], parent=parent)

        self.trw_Explorer.clear()
        lade_cursor = self.conn.cursor()
        explorer_index = []
        ebene_laden(self.rootNode, 1)

    def trw_Explorer_doubleClicked(self, item_index, item_direkt=None):
        """Funktion, die ausgeführt wird, wenn ein Item im Explorer doppelt geklickt wird."""
        # Das zugehörige Explorer Item bekommen

        # Möglicherweise wird dass Item direkt übergeben, nämlich dann, wenn die Funktion manuell aufgerufen wurde.
        if item_direkt:
            item = item_direkt
        else:
            item = self.trw_Explorer.itemFromIndex(item_index)

        # if not isinstance(item, ExplorerItem):  # Eine Fehlerprüfung zur Sicherheit
        #     print("Nicht Explorer Item")
        #     return

        # Wenn ein Vociset doppeltgeklickt wurde, sollten die entsprechenden Daten geladen werden
        if item.typ == "vociset":
            self.kartenModel.lade_daten(item.id)
            self.geladenes_set_explorer_item = item

        # Alte Aktive entfernen
        for altesAktivesItem in self.aktiveItems:
            altesAktivesItem.setActive(False)

        # Aktiv Setzen vom Set und der Hirarchie darüber
        while item.parent():
            item.setActive(True)
            self.aktiveItems.append(item)
            item = item.parent()
        item.setActive(True)
        self.aktiveItems.append(item)

    def trw_Explorer_dragEnterEvent(self, event: QDragEnterEvent):
        """Funktion, die ausgeführt wird, wenn der Benutzer eine DragAndDrop beginnt."""
        if event.source() == self.trw_Explorer:
            event.acceptProposedAction()
        else:
            print("dragEnterEvent nicht zugelassen")

    def trw_Explorer_dropEvent(self, event: QDropEvent):
        """Dies ist die essenzielle DragAndDrop Funktion."""
        # Quell- und Zielitem ermitteln
        # quell_item: ExplorerItem = event.source().currentItem()
        ziel_item: ExplorerItem = self.trw_Explorer.itemAt(event.pos())

        # Wenn ins nichts gezogen wurde..
        if not ziel_item:
            ziel_item = ExplorerItem("ROOT_NODE", "ordner", 1, None)

        if ziel_item.typ == "vociset":
            if ziel_item.parent():
                neue_id = ziel_item.parent().id
            else:  # Das RootItem gibt hier None zurück, es hat die Id 1
                neue_id = 1
        else:
            neue_id = ziel_item.id

        quell_items = []
        ausgewaehlte_items: List[ExplorerItem] = self.trw_Explorer.selectedItems()

        # SQL-Cursor erstellen
        cursor = self.conn.cursor()

        # Alte Aktive entfernen
        for altesAktivesItem in self.aktiveItems:
            altesAktivesItem.setActive(False)

        for ausgewaehltes_item in ausgewaehlte_items:
            id = ausgewaehltes_item.id
            typ = ausgewaehltes_item.typ

            # ****** Änderung an der Datenbank vornehmen ******
            if typ == "ordner":
                query = "UPDATE ordner SET urordner_id = ? WHERE ordner_id = ?"
            elif typ == "vociset":
                query = "UPDATE vociset SET urordner_id = ? WHERE set_id = ?"
            else:
                print("Fehler, DropItem hat kein korrekter Typ")
                return

            cursor.execute(query, (neue_id, id))

            # ****** Änderung im Explorer vornehmen ******

            # Wenn im Ursprungsrdner danach keine Items mehr sind, Ordner als geschlossen anzeigen
            if ausgewaehltes_item.parent():
                print("Das geht")
                print(ausgewaehltes_item.parent().childCount())
                if ausgewaehltes_item.parent().childCount() == 1:
                    ausgewaehltes_item.parent().setExpanded(False)

            # Item am alten Ort löschen
            if ausgewaehltes_item.parent():
                ausgewaehltes_item.parent().removeChild(ausgewaehltes_item)
            else:  # RootNode
                self.rootNode.removeChild(ausgewaehltes_item)

            # Item am neuen Ort hinzufügen
            if ziel_item.typ == "ordner":
                if ziel_item.id == 1:  # Root Ordner
                    self.rootNode.addChild(ausgewaehltes_item)
                else:  # Normaler Ordner
                    ziel_item.addChild(ausgewaehltes_item)

            elif ziel_item.typ == "vociset":
                # Wenn über einem Vociset gedroppt wird, soll das Item im selben Ordner landen
                if ziel_item.parent():
                    ziel_item.parent().addChild(ausgewaehltes_item)
                else:  # Der übergeordnete Ordner ist der Root Ordner
                    self.rootNode.addChild(ausgewaehltes_item)

            # Aktiv Setzen vom Set und der Hirarchie darüber
            item = self.geladenes_set_explorer_item
            try:
                while item.parent():
                    item.setActive(True)
                    self.aktiveItems.append(item)
                    item = item.parent()
                item.setActive(True)
                self.aktiveItems.append(item)
                item = item.parent()
            except AttributeError:  # Am Root Node angekommen
                pass

        # Prozess abschliessen
        cursor.close()
        self.conn.commit()

        # Explorer komplett neu aktualisieren
        # self.trw_Explorer.clear()
        # self.load_explorer()

        event.acceptProposedAction()

    def trw_Explorer_Kontextmenu(self, point: QPoint):
        """Das Kontextmenü für den Explorer anzeigen"""

        # Element, das geklickt wurde herausfinden
        self.kontext_elemente = self.trw_Explorer.selectedItems()

        kontext = QMenu(self)
        kontext.setStyleSheet("selection-background-color: rgb(201, 220, 225);selection-color: rgb(0, 0, 0);")

        aktualisieren = QAction("Aktualisieren", self)
        aktualisieren.setIcon(QIcon("res/icons/refresh_FILL0_wght500_GRAD0_opsz40.svg"))
        aktualisieren.triggered.connect(self.trw_Explorer_Kontextmenu_Aktualisieren)
        kontext.addAction(aktualisieren)

        loeschen = QAction("Löschen", self)
        loeschen.setIcon(QIcon("res/icons/delete_FILL0_wght500_GRAD0_opsz40.svg"))
        loeschen.triggered.connect(self.trw_Explorer_Kontextmenu_Loeschen)
        kontext.addAction(loeschen)

        kontext.exec_(self.trw_Explorer.viewport().mapToGlobal(point))

    def trw_Explorer_Kontextmenu_Aktualisieren(self):
        """'Aktualisieren' Option aus dem Kontextmenu ausführen"""
        self.aktiveItems = []
        self.trw_Explorer.clear()
        self.load_explorer()

    def trw_Explorer_Kontextmenu_Loeschen(self):
        """'Löschen' Option aus dem Kontextmenu ausführen"""
        self.exploreritems_loeschen(self.kontext_elemente)

    def exploreritems_loeschen(self, items):
        """Löscht Elemente aus dem Explorer"""
        print(items)  # todo Hier Lösch Option bauen

    def keyPressEvent(self, event: QKeyEvent, *args, **kwargs):
        """Überschreibung der bereits bestehenden Methode"""

        # Wenn im Explorer Items gelöscht werden wollen:
        if event.key() == Qt.Key_Delete and self.trw_Explorer.hasFocus():
            self.exploreritems_loeschen(self.trw_Explorer.selectedItems())

    def mn_Herunterladen_triggered(self):
        self.mp_Herunterladen = MpHerunterladen(self)
        self.mp_Herunterladen.setModal(True)

        self.mp_Herunterladen.exec_()

    def mn_CSV_importieren_triggered(self):
        """Das CSV-Importieren Fenster wird über das Menu geöffnet."""
        self.importCSV = ImportCSV(self)
        self.importCSV.setModal(True)

        self.importCSV.exec_()

    def mn_Hochladen_triggered(self):
        """Das Fenster um das momentan offene Set hochzuladen wird geöffnet"""
        erfolg, net = log_reg()

        if not erfolg:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Vocitrainer - Fehler")
            msg.setText(
                "Fehler bei der Verbindung / Authentifizierung mit dem Server!"
            )
            msg.exec_()
            return

        offenes_set = self.kartenModel.geladenesSet
        self.mp_Hochladen = MpHochladen(net, offenes_set)
        self.mp_Hochladen.setModal(True)
        self.mp_Hochladen.exec_()
