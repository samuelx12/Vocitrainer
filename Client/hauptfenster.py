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
from Client.res.ui_hauptfenster import Ui_MainWindow
from trainingsfenster import Trainingsfenster
from Mp_herunterladen import MpHerunterladen
from Mp_Hochladen import MpHochladen
from Mp_hochgeladeneVerwalten import MpHochgeladeneVerwalten
from ueber import Ueber as Ueber_Fenster
from importCSV import ImportCSV
from typing import List
from Mp_LogReg import log_reg
from karte_tuple import Karte
import ressources_rc
from rich import print as rprint


class Hauptfenster(QMainWindow, Ui_MainWindow):
    """
    Diese Klasse repräsentiert das Hauptfenster. Sie erbt das Aussehen von der vom Qt-Designer exportierten Klasse.
    Dieses befindet sich in einer eigenen Datei, was den Workflow erheblich erleichtert, weil gleich die ganze
    Datei ohne Gefahr neu überschrieben werden kann.
    """

    def __init__(self, version: str, *args, **kwargs):
        super(Hauptfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Vocitrainer")
        self.setWindowIcon(QIcon("res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"))
        self.version = version

        self.set_angezeigt = False
        self.liste_sichtbar(False)

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite/6), int(hoehe/6), int(breite*2/3), int(hoehe*2/3))

        # Splitter richtig einteilen
        self.splitter.setSizes([100, 300])
        self.splitter.updateGeometry()

        # ---------- Model ----------
        # Tabellen Model erstellen und zuweisen
        self.dbconn = sqlite3.connect('vocitrainerdb.db')
        self.kartenModel = KartenModel(dbconn=self.dbconn)

        # Tabellen Model Daten laden
        self.geladenes_set_explorer_item = None

        # Model zuweisen
        self.tbv_Liste.setModel(self.kartenModel)
        self.tbv_Liste.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tbv_Liste.horizontalHeader().setStretchLastSection(True)

        # ---------- Explorer vorbereiten ----------
        self.rootNode = self.trw_Explorer.invisibleRootItem()
        self.load_explorer()
        self.trw_Explorer.setDragEnabled(True)
        self.trw_Explorer.setAcceptDrops(True)
        self.trw_Explorer.setDropIndicatorShown(True)
        self.trw_Explorer.setDefaultDropAction(Qt.MoveAction)
        self.trw_Explorer.setSelectionMode(QTreeWidget.ExtendedSelection)

        # Aktives Element im Explorer speichern
        self.aktiveItems = []

        # ---------- Signals und Slots verbinden ----------
        # Ribbon Leiste
        self.cmd_SetLernen.clicked.connect(self.cmd_Setlernen_clicked)
        self.cmd_SetUeben.clicked.connect(self.cmd_SetUeben_clicked)
        self.cmd_Lernen.clicked.connect(self.cmd_Lernen_clicked)
        self.cmd_MarkierteLernen.clicked.connect(self.cmd_MarkierteLernen_clicked)
        self.cmd_Einstellungen.clicked.connect(self.cmd_Einstellungen_clicked)
        self.cmd_Beenden.clicked.connect(self.cmd_Beenden_clicked)

        # Menü 'Vocitrainer'
        self.mn_NeuesSet.triggered.connect(self.mn_NeuesSet_triggered)
        self.mn_NeuerOrdner.triggered.connect(self.mn_NeuerOrdner_triggered)
        self.mn_Ueber.triggered.connect(self.mn_Ueber_triggered)
        self.mn_Beenden.triggered.connect(self.mn_Beenden_triggered)

        # Menü 'Lernen'
        self.mn_SetLernen.triggered.connect(self.mn_Lernen_triggered)
        self.mn_SetUeben.triggered.connect(self.mn_SetUeben_triggered)
        self.mn_AusgewaehlteLernen.triggered.connect(self.mn_MarkierteLernen_triggered)
        self.mn_MarkierteLernen.triggered.connect(self.mn_MarkierteLernen_triggered)

        # Menü 'Marketplace'
        self.mn_Herunterladen.triggered.connect(self.mn_Herunterladen_triggered)
        self.mn_Hochladen.triggered.connect(self.mn_Hochladen_triggered)
        self.mn_HochgeladeneVerwalten.triggered.connect(self.mn_hochgeladeneVerwalten_triggered)
        self.mn_Profil.triggered.connect(self.mn_Profil_triggered)

        # Menü 'Importieren'
        self.mn_CSV_importieren.triggered.connect(self.mn_CSV_importieren_triggered)

        # Kontextmenüs aktivieren
        self.trw_Explorer.setContextMenuPolicy(Qt.CustomContextMenu)
        self.trw_Explorer.customContextMenuRequested.connect(self.trw_Explorer_Kontextmenu)

        # Andere Signale
        self.trw_Explorer.doubleClicked.connect(self.trw_Explorer_doubleClicked)
        self.trw_Explorer.dragEnterEvent = self.trw_Explorer_dragEnterEvent
        self.trw_Explorer.dropEvent = self.trw_Explorer_dropEvent

    def liste_sichtbar(self, sichtbar: bool):
        """Kleine Funktion, welche die Meldung "nichts angezeigt" ausblenden und die Liste einblendet bzw. umgekehrt"""

        self.lbl_nichtsAngezeigt1.setVisible(not sichtbar)
        self.lbl_nichtsAngezeigt2.setVisible(not sichtbar)
        self.tbv_Liste.setVisible(sichtbar)
        self.frame_nichtsAngezeigt.setVisible(not sichtbar)

    def msg_kein_set_aktiv(self):
        """
        Eine kleine Funktion, welche eine Error anzeigt, dass kein Set geöffnet sei.
        Sie wird von den Methoden gerufen, welche die Trainings laden.
        """

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QIcon(':/icons/res/icons/error_FILL0_wght400_GRAD0_opsz24.svg'))
        msg.setWindowTitle("Vocitrainer")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText(
            "Es ist kein Set offen!\n" +
            "Du musst ein Set öffnen, um dieses zu lernen."
        )

        msg.exec_()

    def msg_verbindungsFehler(self):
        """
        Zeigt eine MessageBox an, dass die Verbindung fehlgeschlagen sei.
        :return: None
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QIcon(':/icons/res/icons/wifi_off_FILL0_wght400_GRAD0_opsz24.svg'))
        msg.setWindowTitle("Verbindung fehlgeschlagen")
        msg.setText(
            "Fehler bei der Verbindung mit dem Server!\n"
            + "Überprüfen sie ihre Internetverbindung."
        )
        msg.exec_()

    def cmd_Setlernen_clicked(self):
        """
        Set Lernen
        Der Intelligente Lernmodus lernt ein ganzes Set.
        """
        # Überprüfen, ob überhaupt ein Set gewählt ist.
        if not self.set_angezeigt:
            self.msg_kein_set_aktiv()
            return

        # Daten laden und in das Datenformat konvertieren
        selection_model = self.tbv_Liste.selectionModel()
        gewaehlte_indices = selection_model.selectedRows()
        gewaehlte_zeilen = [index.row() for index in gewaehlte_indices]

        # Das ist für die Schwierigkeit_Training, die nicht in den Kartendaten ist.
        #                                                         V
        gewaehlte_karten = [Karte(*self.kartenModel.daten[zeile], 0) for zeile in gewaehlte_zeilen]

        # print(gewaehlte_karten) # DEBUG Hier entkommentieren um zu sehen, welche Karten ins Training geladen werden

        # Sprache herausfinden
        cursor = self.dbconn.cursor()
        sql = """SELECT sprache FROM main.vociset WHERE set_id = ?"""
        cursor.execute(sql, (self.geladenes_set_explorer_item.id,))
        sprache = cursor.fetchone()[0]

        self.trainingsfenster = Trainingsfenster(gewaehlte_karten, sprache, False, self.dbconn)
        self.trainingsfenster.setModal(True)
        if self.trainingsfenster.oeffnen:
            self.trainingsfenster.exec_()

    def load_explorer(self):
        def ebene_laden(parent, parent_id):
            """
            Diese Funktion ladet Rekursiv die Ordnerstruktur
            """
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
            # print(parent_id)
            result = lade_cursor.fetchall()

            # Resultat in Liste umwandeln
            vocisets = []
            for reihe in result:
                vocisets.append(reihe)

            for i_ordner in ordner:
                neuer_ordner = ExplorerItem(i_ordner[1], "ordner", i_ordner[0], parent=parent)
                ebene_laden(neuer_ordner, i_ordner[0])

            for i_vociset in vocisets:
                ExplorerItem(i_vociset[1], "vociset", i_vociset[0], parent=parent)

        self.trw_Explorer.clear()
        lade_cursor = self.dbconn.cursor()
        ebene_laden(self.rootNode, 1)

    def trw_Explorer_doubleClicked(self, item_index, item_direkt=None):
        """Funktion, die ausgeführt wird, wenn ein Item im Explorer doppelt geklickt wird."""
        # Das zugehörige Explorer Item bekommen

        # Möglicherweise wird dass Item direkt übergeben, nämlich dann, wenn die Funktion manuell aufgerufen wurd
        # um ein Set zu laden
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
            self.set_angezeigt = True
            self.liste_sichtbar(True)

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

        ausgewaehlte_items: List[ExplorerItem] = self.trw_Explorer.selectedItems()

        # SQL-Cursor erstellen
        cursor = self.dbconn.cursor()

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
            except AttributeError:  # Am Root Node angekommen
                pass

        # Prozess abschliessen
        cursor.close()
        self.dbconn.commit()

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
        # noinspection PyUnresolvedReferences
        aktualisieren.triggered.connect(self.trw_Explorer_Kontextmenu_Aktualisieren)
        kontext.addAction(aktualisieren)

        loeschen = QAction("Löschen", self)
        loeschen.setIcon(QIcon("res/icons/delete_FILL0_wght500_GRAD0_opsz40.svg"))
        # noinspection PyUnresolvedReferences
        loeschen.triggered.connect(self.trw_Explorer_Kontextmenu_Loeschen)
        kontext.addAction(loeschen)

        kontext.exec_(self.trw_Explorer.viewport().mapToGlobal(point))

    def trw_Explorer_Kontextmenu_Aktualisieren(self):
        """'Aktualisieren' Option aus dem Kontextmenu ausführen"""
        self.aktiveItems = []
        self.trw_Explorer.clear()
        self.load_explorer()

    def trw_Explorer_Kontextmenu_Loeschen(self):
        """'Löschen Option aus dem Kontextmenu ausführen"""
        self.exploreritems_loeschen(self.kontext_elemente)

    def exploreritems_loeschen(self, items: List[ExplorerItem]):
        """Löscht Elemente aus dem Explorer und alle Daten die sie repräsentieren aus der Datenbank"""

        # Warnung anzeigen, dass das Löschen entgültig ist
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon(':/icons/res/icons/delete_forever_FILL0_wght400_GRAD0_opsz24.svg'))
        msg.setWindowTitle("Löschbestätigung")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setText(
            "Achtung! Der Löschvorgang kann nicht rückgängig gemacht werden.\n"
            + "Wollen sie fortfahren?"
        )
        antwort = msg.exec_()

        if antwort == QMessageBox.No:
            return

        loesch_ids = []
        offenes_set_geloescht = False

        for item in items:
            loesch_ids.append([item.id, item.typ])
            item.setHidden(True)
            if item.id == self.geladenes_set_explorer_item.id:
                offenes_set_geloescht = True

        # rprint("[blue]Lösch Ids:")
        # rprint(loesch_ids)

        # Wenn das offene Set gelöscht wird, darf es nicht mehr in der Tabelle offen sein
        if offenes_set_geloescht:
            self.set_angezeigt = False
            self.liste_sichtbar(False)

        # Datenbankcursor erstellen
        cursor = self.dbconn.cursor()

        for loesch_id in loesch_ids:
            if loesch_id[1] == "ordner":
                sql = """DELETE FROM ordner WHERE ordner_id=?"""
            else:
                sql = """DELETE FROM vociset WHERE set_id=?"""

            cursor.execute(sql, (loesch_id[0],))

        cursor.close()
        self.dbconn.commit()

    def keyPressEvent(self, event: QKeyEvent, *args, **kwargs):
        """Überschreibung der bereits bestehenden Methode"""

        # Wenn im Explorer Items gelöscht werden wollen:
        if event.key() == Qt.Key_Delete and self.trw_Explorer.hasFocus():
            self.exploreritems_loeschen(self.trw_Explorer.selectedItems())

    # -------------------------------------------------------
    # ------------------------ SLOTS ------------------------
    # -------------------------------------------------------

    # --------------- MENÜ-LEISTE ---------------
    def cmd_SetLernen_clicked(self):
        """'Set lernen' Button in der Menü-Leiste geklickt"""
        pass

    def cmd_SetUeben_clicked(self):
        """'Set üben' Button in der Menü-Leiste geklickt"""
        pass

    def cmd_Lernen_clicked(self):
        """'Lernen' Button in der Menü-Leiste geklickt"""
        pass

    def cmd_MarkierteLernen_clicked(self):
        """'Markierte lernen' Button in der Menü-Leiste geklickt"""
        pass

    def cmd_Einstellungen_clicked(self):
        """'Einstellungen' Button in der Menü-Leiste geklickt"""
        pass

    def cmd_Beenden_clicked(self):
        """Beenden Button geklickt"""
        self.close()

    # --------------- MENÜ VOCITRAINER ---------------
    def mn_NeuesSet_triggered(self):
        """'Neues Set' Option in dem Vocitrainer-Menü geklickt"""
        pass

    def mn_NeuerOrdner_triggered(self):
        """'Neuer Ordner' Option in dem Vocitrainer-Menü geklickt"""
        pass

    def mn_Einstellungen_triggered(self):
        """'Einstellungen' Option in dem Vocitrainer-Menü geklickt"""
        pass

    def mn_Ueber_triggered(self):
        """Methode zum Aufrufen des Über-Fensters"""
        self.ueber = Ueber_Fenster(self.version)
        self.ueber.setModal(True)

        self.ueber.exec_()

    def mn_Beenden_triggered(self):
        """Wir aufgerufen, wenn im Menü beenden geklickt wird."""
        self.close()

    # --------------- MENÜ LERNEN ---------------
    def mn_SetLernen_triggered(self):
        """'Set lernen' Option in dem Lernen-Menü geklickt"""
        pass

    def mn_SetUeben_triggered(self):
        """'Set üben' Option in dem Lernen-Menü geklickt"""
        pass

    def mn_Lernen_triggered(self):
        """'Lernen' Option in dem Lernen-Menü geklickt"""
        pass

    def mn_MarkierteLernen_triggered(self):
        """'MarkierteLernen' Option in dem Lernen-Menü geklickt"""
        pass

    # --------------- MENÜ MARKETPLACE ---------------
    def mn_Herunterladen_triggered(self):
        """Wird ausgeführt, wenn der Benutzer das Herunterladenmenü anwählt."""
        try:
            self.mp_Herunterladen = MpHerunterladen(self)
        except:
            self.msg_verbindungsFehler()
            return

        self.mp_Herunterladen.setModal(True)

        self.mp_Herunterladen.exec_()

    def mn_Hochladen_triggered(self):
        """Das Fenster um das momentan offene Set hochzuladen wird geöffnet"""

        if not self.set_angezeigt:
            # Es ist kein Set angezeigt, auch wenn dass kartenModel noch das alte Set geladen hat.
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(QIcon(':/icons/res/icons/error_FILL0_wght400_GRAD0_opsz24.svg'))
            msg.setWindowTitle("Kein Set gewählt")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText(
                "Es ist kein Set offen!\n" +
                "Du musst ein Set öffnen, um dieses hochzuladen."
            )

        erfolg, net = log_reg()

        if not erfolg:
            self.msg_verbindungsFehler()
            return

        offenes_set = self.kartenModel.geladenesSet
        self.mp_Hochladen = MpHochladen(net, offenes_set)
        self.mp_Hochladen.setModal(True)
        self.mp_Hochladen.exec_()

    def mn_hochgeladeneVerwalten_triggered(self):
        """Das Fenster um hochgeladene Sets zu verwalten öffnen"""
        erfolg, net = log_reg()

        if not erfolg:
            self.msg_verbindungsFehler()
            return

        self.mp_hochgeladeneVerwalten = MpHochgeladeneVerwalten(net)
        self.mp_hochgeladeneVerwalten.setModal(True)
        self.mp_hochgeladeneVerwalten.exec_()

    def mn_Profil_triggered(self):
        """Wird aufgerufen, wenn im Marcetplace Menü 'Profil' geklickt wird."""

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QIcon(':/icons/res/icons/event_upcoming_FILL0_wght400_GRAD0_opsz24.svg'))
        msg.setWindowTitle("Coming soon")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText(
            "Dieses Feature ist noch nicht hinzugefügt.\n" +
            "Es wird aber bald kommen."
        )
        msg.exec_()

    # --------------- MENÜ IMPORTIEREN ---------------
    def mn_CSV_importieren_triggered(self):
        """Das CSV-Importieren Fenster wird über das Menu geöffnet."""
        self.importCSV = ImportCSV(self)
        self.importCSV.setModal(True)

        self.importCSV.exec_()
