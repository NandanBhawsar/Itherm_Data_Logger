import sys
import sqlite3
from datetime import datetime
from collections import deque

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyqtgraph as pg

from polling import log_values, write_setpoint

HIGH_TEMP = 100
LOW_TEMP = 10


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Itherm Monitor")

        # Initialize alarm state tracking variables
        self.high_alarm_active = False
        self.low_alarm_active = False

        self.db = sqlite3.connect("app.db")
        self.cursor = self.db.cursor()

        layout = QVBoxLayout()

        self.pv_label = QLabel("PV")
        self.sp_label = QLabel("SP")
        self.out_label = QLabel("OUT")
        self.status_label = QLabel("OFFLINE")

        layout.addWidget(self.pv_label)
        layout.addWidget(self.sp_label)
        layout.addWidget(self.out_label)
        layout.addWidget(self.status_label)

        self.alarm_label = QLabel("NO ALARMS")
        layout.addWidget(self.alarm_label)

        self.sp_input = QLineEdit()
        self.sp_input.setPlaceholderText("Enter Setpoint")
        self.sp_input.returnPressed.connect(self.set_sp)
        layout.addWidget(self.sp_input)

        self.set_button = QPushButton("SET")
        self.set_button.clicked.connect(self.set_sp)
        layout.addWidget(self.set_button)

        self.graph = pg.PlotWidget()
        self.graph.setTitle("Process Value")
        self.graph.setLabel("left", "Temperature")
        self.graph.setLabel("bottom", "Samples")
        layout.addWidget(self.graph)

        self.pv_data = deque(maxlen=100)
        for _ in range(100):
            self.pv_data.append(0)

        self.curve = self.graph.plot(list(self.pv_data))

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(2000)

    def set_sp(self):
        try:
            value = float(self.sp_input.text())
            write_setpoint(value)
            print(f"SP set to {value}")
        except Exception as e:
            print(e)

    def update_values(self):
        try:
            pv, sp, output = log_values()

            self.pv_label.setText(f"PV : {pv} °C")
            self.sp_label.setText(f"SP : {sp} °C")
            self.out_label.setText(f"OUT : {output} %")
            self.status_label.setText("ONLINE")

            self.pv_data.append(pv)
            self.curve.setData(list(self.pv_data))

            if pv > HIGH_TEMP:
                self.alarm_label.setText("HIGH TEMP ALARM")
                if not self.high_alarm_active:
                    self.cursor.execute(
                        "INSERT INTO alarms VALUES(?,?)",
                        (datetime.now().isoformat(), "HIGH TEMP")
                    )
                    self.db.commit()
                    self.high_alarm_active = True

            elif pv < LOW_TEMP:
                self.alarm_label.setText("LOW TEMP ALARM")
                if not self.low_alarm_active:
                    self.cursor.execute(
                        "INSERT INTO alarms VALUES(?,?)",
                        (datetime.now().isoformat(), "LOW TEMP")
                    )
                    self.db.commit()
                    self.low_alarm_active = True

            else:
                self.alarm_label.setText("NORMAL")
                self.high_alarm_active = False
                self.low_alarm_active = False

        except Exception as e:
            self.status_label.setText("OFFLINE")
            print(e)


app = QApplication(sys.argv)
window = Window()
window.resize(600, 500)
window.show()
app.exec()