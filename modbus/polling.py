DEMO_MODE = True

import json
import minimalmodbus
import sqlite3

from datetime import datetime

from utils.serial_utils import detect_com_port
from modbus.register_maps import PV, SP, OUTPUT


with open("config.json") as f:

    config = json.load(f)

COM_PORT = config["com_port"]

if not COM_PORT:

    COM_PORT = detect_com_port()

print("COM PORT:", COM_PORT)

BAUDRATE = config["baudrate"]

SLAVE_ID = config["slave_id"]


db = sqlite3.connect("app.db")
cursor = db.cursor()


def connect():

    global instrument

    instrument = minimalmodbus.Instrument(
        COM_PORT,
        SLAVE_ID
    )

    instrument.serial.baudrate = BAUDRATE
    instrument.serial.bytesize = 8
    instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 1

    instrument.mode = minimalmodbus.MODE_RTU


def reconnect():

    try:

        connect()

        print("Reconnected")

        return True

    except Exception as e:

        print("Reconnect failed:", e)

        return False


if not DEMO_MODE:

    connect()


def get_values():

    pv = instrument.read_register(
        PV,
        1,
        signed=True
    )

    sp = instrument.read_register(
        SP,
        1
    )

    output = instrument.read_register(
        OUTPUT,
        1
    )

    return pv, sp, output


def log_values():

    if DEMO_MODE:

        return (
            55,
            60,
            25
        )

    pv, sp, output = get_values()

    cursor.execute(
        "INSERT INTO logs VALUES(?,?,?,?)",
        (
            datetime.now().isoformat(),
            pv,
            sp,
            output
        )
    )

    db.commit()

    return pv, sp, output


def write_setpoint(value):

    if DEMO_MODE:

        print(
            f"Demo SP set to {value}"
        )

        return

    instrument.write_register(
        SP,
        value,
        1
    )