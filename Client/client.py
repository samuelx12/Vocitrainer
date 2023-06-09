# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
import sys
from hauptfenster import Hauptfenster

app = QApplication(sys.argv)

window = Hauptfenster()
window.show()

# Start der Event loop
app.exec()
