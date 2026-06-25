from serial.tools import list_ports


def detect_com_port():

    ports = list(list_ports.comports())

    usb_ports = []

    for port in ports:

        if "USB" in str(port.description).upper():

            usb_ports.append(
                port.device
            )

    if len(usb_ports) == 1:

        return usb_ports[0]

    return None