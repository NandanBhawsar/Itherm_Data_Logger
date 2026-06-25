import json

from PyQt6.QtWidgets import *


class SettingsWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Settings")

        layout = QVBoxLayout()

        self.com = QLineEdit()
        self.baud = QLineEdit()
        self.slave = QLineEdit()

        self.load_settings()

        layout.addWidget(QLabel("COM Port"))
        layout.addWidget(self.com)

        layout.addWidget(QLabel("Baudrate"))
        layout.addWidget(self.baud)

        layout.addWidget(QLabel("Slave ID"))
        layout.addWidget(self.slave)

        save_button = QPushButton("Save")

        save_button.clicked.connect(
            self.save_settings
        )

        layout.addWidget(save_button)

        self.setLayout(layout)

    def load_settings(self):

        with open("config.json") as f:

            data = json.load(f)

        self.com.setText(
            str(data["com_port"])
        )

        self.baud.setText(
            str(data["baudrate"])
        )

        self.slave.setText(
            str(data["slave_id"])
        )

    def save_settings(self):

        data = {

            "com_port":
                self.com.text(),

            "baudrate":
                int(self.baud.text()),

            "slave_id":
                int(self.slave.text())
        }

        with open(
            "config.json",
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )