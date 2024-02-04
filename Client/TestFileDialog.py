from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QVBoxLayout
import sys

class SaveFileDialogExample(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        save_button = QPushButton('Datei speichern')
        save_button.clicked.connect(self.show_save_dialog)

        layout.addWidget(save_button)
        self.setLayout(layout)

    def show_save_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog  # Verwenden Sie den nativen Dateidialog des Betriebssystems nicht

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)  # Einstellen auf Speichermodus

        # Setzen Sie den vorgeschlagenen Dateinamen und den Filter für die Dateierweiterung
        file_dialog.setDefaultSuffix('vocidb')
        file_dialog.setNameFilter("Vocidb Dateien (*.vocidb);;Alle Dateien (*)")

        # Anpassen des Dialogtitels
        file_dialog.setWindowTitle("Exportieren")
        file_dialog.setLabelText(QFileDialog.Accept, "Exportieren")

        # Dialog anzeigen und das Ergebnis überprüfen
        result = file_dialog.exec_()
        if result == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            print("Gewählte Datei zum Speichern:", selected_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SaveFileDialogExample()
    window.show()
    sys.exit(app.exec_())
