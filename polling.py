import minimalmodbus
import sqlite3

from datetime import datetime
from registers import PV, SP, OUTPUT

instrument = minimalmodbus.Instrument(
    'COM6',
    1
)

instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout = 1

instrument.mode = minimalmodbus.MODE_RTU

db = sqlite3.connect("app.db")
cursor = db.cursor()


def get_values():

    pv = instrument.read_register(PV, 1,signed=True)

    sp = instrument.read_register(SP, 1)

    output = instrument.read_register(
        OUTPUT,
        1
    )

    return pv, sp, output


def log_values():

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

    instrument.write_register(
        SP,
        value,
        1
    )