from database.db import init_db

from PyQt6.QtWidgets import QApplication

from gui.dashboard import Window

import sys

init_db()

app = QApplication(sys.argv)

window = Window()

window.show()

app.exec()