from modbus.device_profiles import DEVICES
from datetime import datetime
from collections import deque
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from gui.history import HistoryWindow

from gui.settings import SettingsWindow

from gui.alarm_history import (
    AlarmHistoryWindow
)

from exports.csv_export import (
    export_logs
)
import pyqtgraph as pg

from modbus.polling import (
    log_values,
    write_setpoint
)

from database.db import (
    get_db
)

HIGH_TEMP = 100
LOW_TEMP = 10


class Window(QWidget):
    
    def __init__(self):
        super().__init__()

        self.resize(1000, 700)

        self.setWindowTitle("Itherm Monitor")

        self.high_alarm_active = False
        self.low_alarm_active = False

        self.db = get_db()
        self.cursor = self.db.cursor()

        layout = QVBoxLayout()

        title = QLabel("ITHERM TEMPERATURE MONITOR")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)
        layout.addWidget(title)

        device_group = QGroupBox("Device Information")
        device_layout = QVBoxLayout()

        self.device_combo = QComboBox()
        self.device_combo.addItems(DEVICES)

        self.status_label = QLabel("OFFLINE")
        self.status_label.setStyleSheet(
            "color:red;font-weight:bold;"
        )

        self.alarm_label = QLabel("NO ALARMS")

        device_layout.addWidget(self.device_combo)
        device_layout.addWidget(self.status_label)
        device_layout.addWidget(self.alarm_label)

        device_group.setLayout(device_layout)

        layout.addWidget(device_group)

        process_group = QGroupBox("Process Values")
        process_layout = QVBoxLayout()

        self.pv_label = QLabel("PV : -- °C")
        self.sp_label = QLabel("SP : -- °C")
        self.out_label = QLabel("OUT : -- %")

        self.pv_label.setStyleSheet(
            "font-size:24px;font-weight:bold;"
        )

        process_layout.addWidget(self.pv_label)
        process_layout.addWidget(self.sp_label)
        process_layout.addWidget(self.out_label)

        process_group.setLayout(process_layout)

        layout.addWidget(process_group)

        control_group = QGroupBox("Setpoint Control")
        control_layout = QHBoxLayout()

        self.sp_input = QLineEdit()
        self.sp_input.setPlaceholderText(
            "Enter Setpoint"
        )

        self.sp_input.returnPressed.connect(
            self.set_sp
        )

        self.set_button = QPushButton("SET")
        self.set_button.clicked.connect(
            self.set_sp
        )

        control_layout.addWidget(self.sp_input)
        control_layout.addWidget(self.set_button)

        control_group.setLayout(control_layout)

        layout.addWidget(control_group)

        self.history_button = QPushButton("History")
        self.history_button.clicked.connect(
            self.open_history
        )

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(
            self.open_settings
        )

        self.alarm_button = QPushButton(
            "Alarm History"
        )
        self.alarm_button.clicked.connect(
            self.open_alarm_history
        )

        self.export_button = QPushButton(
            "Export CSV"
        )
        self.export_button.clicked.connect(
            self.export_csv
        )

        action_group = QGroupBox("Actions")
        action_layout = QHBoxLayout()

        action_layout.addWidget(
            self.history_button
        )
        action_layout.addWidget(
            self.settings_button
        )
        action_layout.addWidget(
            self.alarm_button
        )
        action_layout.addWidget(
            self.export_button
        )

        action_group.setLayout(action_layout)

        layout.addWidget(action_group)

        graph_group = QGroupBox("Trend Graph")
        graph_layout = QVBoxLayout()

        self.graph = pg.PlotWidget()

        self.graph.setTitle(
            "Process Value"
        )

        self.graph.setLabel(
            "left",
            "Temperature"
        )

        self.graph.setLabel(
            "bottom",
            "Samples"
        )

        self.graph.showGrid(
            x=True,
            y=True
        )

        graph_layout.addWidget(
            self.graph
        )

        graph_group.setLayout(
            graph_layout
        )

        layout.addWidget(
            graph_group
        )

        self.pv_data = deque(maxlen=100)

        for _ in range(100):
            self.pv_data.append(0)

        self.curve = self.graph.plot(
            list(self.pv_data)
        )

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(
            self.update_values
        )
        self.timer.start(2000)

       
    def set_sp(self):
        try:
            value = float(self.sp_input.text())
            write_setpoint(value)
            print(f"SP set to {value}")
        except Exception as e:
            print(e)

    def open_history(self):

        self.history = HistoryWindow()

        self.history.show()


    def open_settings(self):

        self.settings = SettingsWindow()

        self.settings.show()


    def open_alarm_history(self):

        self.alarms = AlarmHistoryWindow()

        self.alarms.show()


    def export_csv(self):

        export_logs()

        QMessageBox.information(
            self,
            "Export",
            "CSV Exported"
        )

    def update_values(self):
        try:
            pv, sp, output = log_values()

            self.pv_label.setText(f"PV : {pv} °C")
            self.sp_label.setText(f"SP : {sp} °C")
            self.out_label.setText(f"OUT : {output} %")
           
            self.status_label.setText("ONLINE")
            self.status_label.setStyleSheet(
                "color:green;font-weight:bold;"
            )

            self.pv_data.append(pv)
            self.curve.setData(list(self.pv_data))

            if pv > HIGH_TEMP:
                self.alarm_label.setText("HIGH TEMP ALARM")
                self.alarm_label.setStyleSheet(
                    "background:red;color:white;font-weight:bold;"
                )
                
                if not self.high_alarm_active:
                    self.cursor.execute(
                        "INSERT INTO alarms VALUES(?,?)",
                        (datetime.now().isoformat(), "HIGH TEMP")
                    )
                    self.db.commit()
                    self.high_alarm_active = True

            elif pv < LOW_TEMP:
                self.alarm_label.setText("LOW TEMP ALARM")
                self.alarm_label.setStyleSheet(
                    "background:orange;font-weight:bold;"
                )

                if not self.low_alarm_active:
                    self.cursor.execute(
                        "INSERT INTO alarms VALUES(?,?)",
                        (datetime.now().isoformat(), "LOW TEMP")
                    )
                    self.db.commit()
                    self.low_alarm_active = True

            else:
                self.alarm_label.setText("NORMAL")
                self.alarm_label.setStyleSheet(
                    "background:lightgreen;font-weight:bold;"
                )

                self.high_alarm_active = False
                self.low_alarm_active = False

        except Exception as e:

            self.status_label.setText(
                "OFFLINE"
            )
            self.status_label.setStyleSheet(
                "color:red;font-weight:bold;"
            )

            from modbus.polling import reconnect

            reconnect()

            print(e)


