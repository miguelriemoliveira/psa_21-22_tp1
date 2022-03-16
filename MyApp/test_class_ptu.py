#!/usr/bin/env python3
import time

from ClassPTU import ClassPTU
# -------------------------
# Initialization
# -------------------------

ptu = ClassPTU()
ptu.connect('/dev/ttyUSB0')

# -------------------------
# Execution in cycle
# -------------------------
while True:

    ptu.goal.position.pan = -3000
    ptu.goal.position.tilt = 1500
    ptu.setData()

    # for i in range(0,100):
    ptu.getData()


    time.sleep(3)


    ptu.goal.position.pan = 3000
    ptu.goal.position.tilt = -1500
    ptu.setData()
    ptu.getData()
    time.sleep(5)

    # msg_received = serial_ptu.read_until().decode()
    # print('Received from serial msg: ' + msg_received)
    #
    # time.sleep(5)  # wait 3 seconds
    # # Send pan to 5000
    # msg_to_send = 'PP5000\n'
    # serial_ptu.write(msg_to_send.encode())
    # print('Writting to serial msg: ' + msg_to_send)
    #
    # time.sleep(0.02)
    # msg_received = serial_ptu.read_until().decode()
    # print('Received from serial msg: ' + msg_received)
    #
    # time.sleep(5)  # wait 3 seconds

# -------------------------
# Termination
# -------------------------

serial_ptu.close()