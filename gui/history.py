from PyQt6.QtWidgets import *
import pyqtgraph as pg
import sqlite3

class HistoryWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "History"
        )

        layout = QVBoxLayout()

        self.graph = pg.PlotWidget()

        layout.addWidget(
            self.graph
        )

        self.setLayout(layout)

        self.load_data()

    def load_data(self):

        db = sqlite3.connect(
            "app.db"
        )

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT pv
            FROM logs
            ORDER BY timestamp
            """
        )

        rows = cursor.fetchall()

        values = [
            row[0]
            for row in rows
        ]

        self.graph.clear()

        self.graph.plot(values)