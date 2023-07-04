import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTableView, QVBoxLayout)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(max(self._data, key=len))

    def data(self, index, role=Qt.DisplayRole):
        # display data
        if role == Qt.DisplayRole:
            print('Display role:', index.row(), index.column())
            try:
                return self._data[index.row()][index.column()]
            except IndexError:
                return ''

    def setData(self, index, value, role=Qt.EditRole):
        if role in (Qt.DisplayRole, Qt.EditRole):
            print('Edit role:', index.row(), index.column())
            # if value is blank
            if not value:
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)
        self.setStyleSheet('''
			QWidget {
				font-size: 30px;
			}
		''')

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.table = QTableView()
        self.layout['main'].addWidget(self.table)

        data_model = TableModel(data)
        self.table.setModel(data_model)


if __name__ == '__main__':
    data = [
        ['A1', 'A2', 'A3'],
        ['B1', 'B2', 'B3', 'B4'],
        ['C1', 'C2', 'C3', 'C4', 'C5']
    ]

    # row count
    # print(len(data))

    # column count
    # print(len(max(data, key=len)))

    app = QApplication(sys.argv)

    myApp = MainApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

2