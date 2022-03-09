#!/usr/bin/env python3
import time

import serial

# -------------------------
# Initialization
# -------------------------

serial_ptu = serial.Serial()

# Configuration of serial communication parameters
serial_ptu.port = '/dev/ttyUSB0'
serial_ptu.baudrate = 9600
serial_ptu.bytesize = 8
serial_ptu.stopbits = 1
serial_ptu.parity = serial.PARITY_NONE
serial_ptu.xonxoff = False
serial_ptu.rtscts = False
serial_ptu.dsrdtr = False
serial_ptu.timeout = 1

serial_ptu.open()

# -------------------------
# Execution in cycle
# -------------------------
while True:
    # Send pan to -5000
    msg_to_send = 'PP-5000\n'
    serial_ptu.write(msg_to_send.encode())
    print('Writting to serial msg: ' + msg_to_send)

    time.sleep(0.02)
    msg_received = serial_ptu.read_until().decode()
    print('Received from serial msg: ' + msg_received)

    time.sleep(5)  # wait 3 seconds
    # Send pan to 5000
    msg_to_send = 'PP5000\n'
    serial_ptu.write(msg_to_send.encode())
    print('Writting to serial msg: ' + msg_to_send)

    time.sleep(0.02)
    msg_received = serial_ptu.read_until().decode()
    print('Received from serial msg: ' + msg_received)

    time.sleep(5)  # wait 3 seconds

# -------------------------
# Termination
# -------------------------

serial_ptu.close()
