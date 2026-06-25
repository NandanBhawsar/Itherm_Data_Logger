from PyQt6.QtWidgets import *

import sqlite3


class AlarmHistoryWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Alarm History"
        )

        layout = QVBoxLayout()

        self.table = QTableWidget()

        layout.addWidget(
            self.table
        )

        refresh = QPushButton(
            "Refresh"
        )

        refresh.clicked.connect(
            self.load_data
        )

        layout.addWidget(
            refresh
        )

        self.setLayout(layout)

        self.load_data()

    def load_data(self):

        db = sqlite3.connect(
            "app.db"
        )

        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM alarms"
        )

        rows = cursor.fetchall()

        self.table.setRowCount(
            len(rows)
        )

        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(
            [
                "Timestamp",
                "Alarm"
            ]
        )

        for r, row in enumerate(rows):

            for c, value in enumerate(row):

                self.table.setItem(
                    r,
                    c,
                    QTableWidgetItem(
                        str(value)
                    )
                )