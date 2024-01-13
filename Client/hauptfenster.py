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
from res.ui_hauptfenster import Ui_MainWindow
from trainingsfenster import Trainingsfenster
from Mp_herunterladen import MpHerunterladen
from Mp_Hochladen import MpHochladen
from Mp_hochgeladeneVerwalten import MpHochgeladeneVerwalten
from ueber import Ueber as Ueber_Fenster
from neuesWort import NeuesWort
from importCSV import ImportCSV
from typing import List, Union
from Mp_LogReg import log_reg
from karte_tuple import Karte
from einstellungen import Einstellungen
import ressources_rc
from rich import print as rprint


class Hauptfenster(QMainWindow, Ui_MainWindow):
    """
    Diese Klasse repräsentiert das Hauptfenster. Sie erbt das Aussehen von der vom Qt-Designer exportierten Klasse.
    Dieses befindet sich in einer eigenen Datei, was den Workflow erheblich erleichtert, weil gleich die ganze
    Datei ohne Gefahr neu überschrieben werden kann.
    """

    def __init__(self, versionen: dict, *args, **kwargs):
        super(Hauptfenster, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Vocitrainer")
        # self.setWindowIcon(QIcon("res/icons/note_stack_FILL0_wght500_GRAD0_opsz40.svg"))
        self.versionen = versionen

        self.set_angezeigt = False
        self.liste_sichtbar(False)

        # Bildschirmgrösse setzen
        bildschirm_geometrie = QDesktopWidget().screenGeometry(QDesktopWidget().primaryScreen())
        breite = bildschirm_geometrie.width()
        hoehe = bildschirm_geometrie.height()
        self.setGeometry(int(breite/6), int(hoehe/6), int(breite*1/2), int(hoehe*2/3))

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
        # self.tbv_Liste.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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
        self.cmd_SetLernen.clicked.connect(self.cmd_SetLernen_clicked)
        self.cmd_SetUeben.clicked.connect(self.cmd_SetUeben_clicked)
        self.cmd_Lernen.clicked.connect(self.cmd_Lernen_clicked)
        self.cmd_MarkierteLernen.clicked.connect(self.cmd_MarkierteLernen_clicked)
        self.cmd_Einstellungen.clicked.connect(self.cmd_Einstellungen_clicked)
        self.cmd_Beenden.clicked.connect(self.cmd_Beenden_clicked)

        # Menü 'Vocitrainer'
        self.mn_NeuesSet.triggered.connect(self.mn_NeuesSet_triggered)
        self.mn_NeuerOrdner.triggered.connect(self.mn_NeuerOrdner_triggered)
        self.mn_Einstellungen.triggered.connect(self.mn_Einstellungen_triggered)
        self.mn_Ueber.triggered.connect(self.mn_Ueber_triggered)
        self.mn_Beenden.triggered.connect(self.mn_Beenden_triggered)

        # Menü 'Lernen'
        self.mn_SetLernen.triggered.connect(self.mn_Lernen_triggered)
        self.mn_SetUeben.triggered.connect(self.mn_SetUeben_triggered)
        self.mn_AusgewaehlteLernen.triggered.connect(self.mn_MarkierteLernen_triggered)
        self.mn_MarkierteLernen.triggered.connect(self.mn_MarkierteLernen_triggered)

        # Menü 'Set'
        self.mn_WoerterHinzufuegen.triggered.connect(self.mn_WoerterHinzufuegen_triggered)
        self.mn_AusgewaehlteWoerterLoeschen.triggered.connect(self.mn_AusgewaehlteWoerterLoeschen_triggered)
        self.mn_FortschrittZuruecksetzen.triggered.connect(self.mn_FortschrittZuruecksetzen_triggered)

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
        """
        Kleine Funktion, welche die Meldung "nichts angezeigt" ausblenden und die Liste einblendet bzw. umgekehrt.
        Zudem werden die Lernen-Buttons und die Hochladen-Funktion disabled bzw. enabled.
        """

        self.lbl_nichtsAngezeigt1.setVisible(not sichtbar)
        self.lbl_nichtsAngezeigt2.setVisible(not sichtbar)
        self.tbv_Liste.setVisible(sichtbar)
        self.frame_nichtsAngezeigt.setVisible(not sichtbar)

        self.cmd_SetLernen.setEnabled(sichtbar)
        self.cmd_SetUeben.setEnabled(sichtbar)
        self.cmd_Lernen.setEnabled(sichtbar)
        self.cmd_MarkierteLernen.setEnabled(sichtbar)

        self.mn_SetLernen.setEnabled(sichtbar)
        self.mn_SetUeben.setEnabled(sichtbar)
        self.mn_AusgewaehlteLernen.setEnabled(sichtbar)
        self.mn_MarkierteLernen.setEnabled(sichtbar)

        self.mn_WoerterHinzufuegen.setEnabled(sichtbar)
        self.mn_AusgewaehlteWoerterLoeschen.setEnabled(sichtbar)
        self.mn_FortschrittZuruecksetzen.setEnabled(sichtbar)

        self.mn_Hochladen.setEnabled(sichtbar)

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
            "Du musst ein Set öffnen, um dieses zu lernen oder zu bearbeiten."
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
                ExplorerItem(i_vociset[1], "vociset", i_vociset[0], parent, i_vociset[3], i_vociset[2])

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
            if self.geladenes_set_explorer_item:
                if item.id == self.geladenes_set_explorer_item.id:
                    offenes_set_geloescht = True

        # rprint("[blue]Lösch Ids:")
        # rprint(loesch_ids)

        # Wenn das offene Set gelöscht wird, darf es nicht mehr in der Tabelle offen sein
        if offenes_set_geloescht:
            self.set_angezeigt = False
            self.liste_sichtbar(False)
            self.geladenes_set_explorer_item = None

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

        if event.key() == Qt.Key_Delete and self.tbv_Liste.hasFocus():
            self.mn_AusgewaehlteWoerterLoeschen_triggered()

    def einstellungen_oeffnen(self):
        """Diese Funktion öffneet die Einstellungen."""
        einstellungen = Einstellungen()
        einstellungen.setModal(True)
        einstellungen.exec_()

    def lernen(self, controller: str, quelle: Union[0, 1, 2]) -> None:
        """
        Diese Funktion startet das Training.
        :param controller: Welcher Trainings_Controller verwendet werden sollen
        :param quelle: Ob alle Karten des Sets, nur Ausgewählte oder Markierte gelernt werden sollen.
            0 => Alle
            1 => Nur Ausgewählte
            2 => Nur Markierte
        :return: None
        """
        # Überprüfen, ob überhaupt ein Set gewählt ist.
        if not self.set_angezeigt:
            self.msg_kein_set_aktiv()
            return

        ausgewaehlte_vorhanden = False
        if quelle == 1:
            # Nur Ausgewählte Daten laden
            selection_model = self.tbv_Liste.selectionModel()
            gewaehlte_indices = selection_model.selectedRows()
            karte_zeile = [index.row() for index in gewaehlte_indices]
            if karte_zeile:
                ausgewaehlte_vorhanden = True

        if quelle == 0 or quelle == 2 or not ausgewaehlte_vorhanden:
            # Alle Daten laden und in das Datenformat konvertieren
            karte_zeile = [row for row in range(self.tbv_Liste.model().rowCount())]

        # Das ist für den Schwierigkeit_Training Wert, der nicht in den Kartendaten ist.
        #                                                         V
        gewaehlte_karten_1 = [Karte(*self.kartenModel.daten[zeile], 0) for zeile in karte_zeile]

        # Falls nur Markierte gewünscht alle anderen aussortieren
        # Sonst einfach übernehmen
        gewaehlte_karten_2 = []
        if quelle == 2:
            for gewaehlte_karte in gewaehlte_karten_1:
                if gewaehlte_karte.markiert:
                    gewaehlte_karten_2.append(gewaehlte_karte)
        else:
            gewaehlte_karten_2 = gewaehlte_karten_1

        if not gewaehlte_karten_2:
            # Falls keine Karten geladen wurden
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(QIcon(':/icons/res/icons/error_FILL0_wght400_GRAD0_opsz24.svg'))
            msg.setWindowTitle("Vocitrainer")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText(
                "Es konnten keine Vokabeln geladen werden!\n" +
                "Überprüfe, ob das Set (markierte) Karten enthält."
            )
            msg.exec_()
            return

        # Sprache herausfinden
        cursor = self.dbconn.cursor()
        sql = """SELECT sprache FROM main.vociset WHERE set_id = ?"""
        cursor.execute(sql, (self.geladenes_set_explorer_item.id,))
        sprache = cursor.fetchone()[0]

        # Trainingsfenster öffnen
        self.trainingsfenster = Trainingsfenster(gewaehlte_karten_2, sprache, controller, self.dbconn)
        self.trainingsfenster.setModal(True)
        if self.trainingsfenster.oeffnen:
            self.trainingsfenster.exec_()

    # -------------------------------------------------------
    # ------------------------ SLOTS ------------------------
    # -------------------------------------------------------

    # --------------- MENÜ-LEISTE ---------------
    def cmd_SetLernen_clicked(self):
        """'Set lernen' Button in der Menü-Leiste geklickt"""
        self.lernen("intelligent", 0)

    def cmd_SetUeben_clicked(self):
        """'Set üben' Button in der Menü-Leiste geklickt"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon(':/icons/res/icons/event_upcoming_FILL0_wght400_GRAD0_opsz24.svg'))
        msg.setWindowTitle("Coming soon")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText(
            "Der Trainingsmodus 'Set üben' ist die perfekte Ergänzung zu 'Set lernen'.\n" +
            "Er momentan noch nicht verfügbar, wird aber bald hinzugefügt."
        )
        msg.exec_()

    def cmd_Lernen_clicked(self):
        """'Lernen' Button in der Menü-Leiste geklickt"""
        self.lernen("einfach", 1)

    def cmd_MarkierteLernen_clicked(self):
        """'Markierte lernen' Button in der Menü-Leiste geklickt"""
        self.lernen("einfach", 2)

    def cmd_Einstellungen_clicked(self):
        """'Einstellungen' Button in der Menü-Leiste geklickt"""
        self.einstellungen_oeffnen()

    def cmd_Beenden_clicked(self):
        """Beenden Button geklickt"""
        self.close()

    # --------------- MENÜ VOCITRAINER ---------------
    def mn_NeuesSet_triggered(self):
        """
        'Neues Set' Option in dem Vocitrainer-Menü geklickt
        Ablauf: 1. Informationen einholen, 2. in der DB einfügen, 3. im Explorer einfügen
        """
        # Überstehender Ordner finden
        if self.geladenes_set_explorer_item:
            parent_element = self.geladenes_set_explorer_item.parent()
            if not parent_element:
                parent_element = self.rootNode
        else:
            parent_element = self.rootNode

        # todo Standartsprache für neue Sets einbauen
        sprache = "Englisch"
        # Parent Id herausfinden
        try:
            parent_id = parent_element.id
        except:
            # Root Node
            parent_id = 1

        # In der Datenbank hinzufügen
        cursor = self.dbconn.cursor()
        sql = """
        INSERT INTO vociset (set_name, beschreibung, sprache, urordner_id) VALUES (?, ?, ?, ?)
"""
        cursor.execute(sql, ("Unbenanntes Set", "", sprache, parent_id))

        gespeicherte_set_id = cursor.lastrowid
        cursor.close()
        self.dbconn.commit()

        # Neues Element im Explorer erstellen
        ExplorerItem(
            "Unbenanntes Set",
            "vociset",
            gespeicherte_set_id,
            parent_element,
            "Englisch",
            ""
        )

    def mn_NeuerOrdner_triggered(self):
        """
        'Neuer Ordner' Option in dem Vocitrainer-Menü geklickt
        Ablauf: 1. Informationen einholen, 2. in der DB einfügen, 3. im Explorer einfügen
        """
        # Überstehender Ordner finden
        if self.geladenes_set_explorer_item:
            parent_element = self.geladenes_set_explorer_item.parent()
            if not parent_element:
                parent_element = self.rootNode
        else:
            parent_element = self.rootNode

        # Parent Id herausfinden
        try:
            parent_id = parent_element.id
        except:
            # Root Node
            parent_id = 1

        # In der Datenbank hinzufügen
        cursor = self.dbconn.cursor()
        sql = """
        INSERT INTO ordner (ordner_name, urordner_id) VALUES (?, ?)
"""
        cursor.execute(sql, ("Unbenannter Ordner", parent_id))

        gespeicherte_set_id = cursor.lastrowid
        cursor.close()
        self.dbconn.commit()

        # Neues Element im Explorer erstellen
        ExplorerItem(
            "Unbenannter Ordner",
            "ordner",
            gespeicherte_set_id,
            parent_element,
        )

    def mn_Einstellungen_triggered(self):
        """'Einstellungen' Option in dem Vocitrainer-Menü geklickt"""
        self.einstellungen_oeffnen()

    def mn_Ueber_triggered(self):
        """Methode zum Aufrufen des Über-Fensters"""
        self.ueber = Ueber_Fenster(self.versionen)
        self.ueber.setModal(True)

        self.ueber.exec_()

    def mn_Beenden_triggered(self):
        """Wir aufgerufen, wenn im Menü beenden geklickt wird."""
        self.close()

    # --------------- MENÜ LERNEN ---------------
    def mn_SetLernen_triggered(self):
        """'Set lernen' Option in dem Lernen-Menü geklickt"""
        self.lernen("intelligent", 0)
        self.kartenModel.lade_daten(self.geladenes_set_explorer_item.id)

    def mn_SetUeben_triggered(self):
        """'Set üben' Option in dem Lernen-Menü geklickt"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon(':/icons/res/icons/event_upcoming_FILL0_wght400_GRAD0_opsz24.svg'))
        msg.setWindowTitle("Coming soon")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText(
            "Der Trainingsmodus 'Set üben' ist die perfekte Ergänzung zu 'Set lernen'.\n" +
            "Er momentan noch nicht verfügbar, wird aber bald hinzugefügt."
        )
        msg.exec_()

    def mn_Lernen_triggered(self):
        """'Lernen' Option in dem Lernen-Menü geklickt"""
        self.lernen("einfach", 1)

    def mn_MarkierteLernen_triggered(self):
        """'MarkierteLernen' Option in dem Lernen-Menü geklickt"""
        self.lernen("einfach", 2)

    # --------------- MENÜ Set ---------------
    def mn_WoerterHinzufuegen_triggered(self):
        """'Wörtern hinzufügen' Option im Set-Menü geklickt."""

        # Überprüfen, ob überhaupt ein Set gewählt ist.
        if not self.set_angezeigt:
            self.msg_kein_set_aktiv()
            return

        # Fenster mit aufrufen und die Set_Id + Datenbankverbindung mitgeben
        neueWoerter = NeuesWort(self.geladenes_set_explorer_item.id, self.dbconn)
        neueWoerter.exec_()

        self.trw_Explorer_doubleClicked(self.geladenes_set_explorer_item.id, self.geladenes_set_explorer_item)

    def mn_AusgewaehlteWoerterLoeschen_triggered(self):
        """'Ausgewählte Wörter löschen' Option im Set-Menü geklickt."""

        # Überprüfen, ob überhaupt ein Set gewählt ist.
        if not self.set_angezeigt:
            self.msg_kein_set_aktiv()
            return

        # Nur Ausgewählte Daten laden
        selection_model = self.tbv_Liste.selectionModel()
        gewaehlte_indices = selection_model.selectedRows()
        karte_zeilen = [index.row() for index in gewaehlte_indices]

        karte_ids = [self.kartenModel.daten[zeile][0] for zeile in karte_zeilen]

        if not karte_ids:
            # Error wenn keine Sets ausgewählt wurden
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(QIcon(':/icons/res/icons/error_FILL0_wght400_GRAD0_opsz24.svg'))
            msg.setWindowTitle("Fehler")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText(
                "Es sind keine zu löschenden Wörter ausgewählt!"
            )
            msg.exec_()
            return

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

        cursor = self.dbconn.cursor()
        sql = """DELETE FROM karte WHERE karte_id=?"""

        for karte_id in karte_ids:
            print(karte_id)
            cursor.execute(sql, (karte_id,))

        cursor.close()
        self.dbconn.commit()

        self.kartenModel.lade_daten(self.geladenes_set_explorer_item.id)

    def mn_FortschrittZuruecksetzen_triggered(self):
        """
        'Fortschritt zurückseten' Option im Set-Menü geklickt.
        Dabei wird der Lernfortschritt und die Schwierigkeitsdaten für das aktive Lernset gelöscht.
        """
        if not self.set_angezeigt:
            self.msg_kein_set_aktiv()
            return

        # Warnung anzeigen, dass das Löschen entgültig ist
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon(':/icons/res/icons/warning_FILL0_wght400_GRAD0_opsz24.svg'))
        msg.setWindowTitle("Zurücksetzen bestätigen")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setText(
            "Achtung! Das Zurücksetzen des Fortschrittes kann nicht rückgängig gemacht werden.\n"
            + "Wollen sie fortfahren?"
        )
        antwort = msg.exec_()

        if antwort == QMessageBox.No:
            return

        set_id = self.geladenes_set_explorer_item.id

        sql = """UPDATE karte SET lernfortschritt=0, schwierigkeit=-1 WHERE set_id=?"""

        cursor = self.dbconn.cursor()
        cursor.execute(sql, (set_id,))
        cursor.close()
        self.dbconn.commit()

        self.kartenModel.lade_daten(set_id)

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

        self.einstellungen_oeffnen()

    # --------------- MENÜ IMPORTIEREN ---------------
    def mn_CSV_importieren_triggered(self):
        """Das CSV-Importieren Fenster wird über das Menu geöffnet."""
        self.importCSV = ImportCSV(self)
        self.importCSV.setModal(True)

        self.importCSV.exec_()
