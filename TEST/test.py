

import minimalmodbus
import time

instrument = minimalmodbus.Instrument('COM6', 1)

instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_ODD
instrument.serial.stopbits = 1
instrument.serial.timeout = 1

instrument.mode = minimalmodbus.MODE_RTU


#instrument.debug = True
print("Connected")

# while True:
print("PV", instrument.read_register(138, 1,signed=True))
print("SP", instrument.read_register(0, 1))

print("R1", instrument.read_register(1, 1))
print("R135", instrument.read_register(135, 1))
print("R136", instrument.read_register(136, 0))
time.sleep(1)
   