import time

import serial
from ClassAbstractHardware import ClassAbstractHardware

class PanTiltAxis():
    def __init__(self):
        self.pan = None
        self.tilt = None

class PositionSpeed():
    def __init__(self):
        self.position = PanTiltAxis()
        self.speed = PanTiltAxis()

class ClassPTU(ClassAbstractHardware):

    def __init__(self):
        super().__init__() # call super class constructor
        self.goal = PositionSpeed()
        self.current = PositionSpeed()

    def _connect(self, device):
        self.serial = serial.Serial()

        # Configuration of serial communication parameters
        self.serial.port = device
        self.serial.baudrate = 38400
        self.serial.bytesize = 8
        self.serial.stopbits = 1
        self.serial.parity = serial.PARITY_NONE
        self.serial.xonxoff = False
        self.serial.rtscts = False
        self.serial.dsrdtr = False
        self.serial.timeout = 1

        self.serial.open()

        msg_to_send = 'ED\n'
        self.serial.write(msg_to_send.encode())
        return True

    def _disconnect(self):
        self.serial.close()
        return True

    def _setData(self):

        msg_to_send = 'PP' + str(self.goal.position.pan) + '\n'
        self.serial.write(msg_to_send.encode())
        msg_to_send = 'TP' + str(self.goal.position.tilt) + '\n'
        self.serial.write(msg_to_send.encode())
        return False

    def _getData(self):
        # print('get data called')


        msg_to_send = 'PP\n'
        self.serial.write(msg_to_send.encode())
        msg_to_send = 'TP\n'
        self.serial.write(msg_to_send.encode())
        msg_to_send = 'PS\n'
        self.serial.write(msg_to_send.encode())
        msg_to_send = 'TS\n'
        self.serial.write(msg_to_send.encode())

        time.sleep(0.02)

        data_received = self.serial.read_all().decode()
        print(data_received)

        msgs_received = data_received.split('\n')
        print(msgs_received)

        for msg_received in msgs_received:
            msg_received = msg_received.strip('\r')

            # print('Analysing msg =\n' + msg_received)
            if 'Current Pan position is' in msg_received:
                # print('found current pan position')
                self.current.position.pan = self.findFirstNumeric(msg_received)
            elif 'Current Tilt position is' in msg_received:
                # print('found current tilt position')
                self.current.position.tilt= self.findFirstNumeric(msg_received)
            elif 'Target Pan speed is' in msg_received:
                # print('found Pan Speed')
                self.current.speed.pan = self.findFirstNumeric(msg_received)
            elif 'Target Tilt speed is' in msg_received:
                # print('found Tilt speed')
                self.current.speed.tilt= self.findFirstNumeric(msg_received)

        print('current ptu state is:')
        print('current.position.pan = ' + str(self.current.position.pan))
        print('current.position.tilt = ' + str(self.current.position.tilt))
        print('current.speed.pan = ' + str(self.current.speed.pan))
        print('current.speed.tilt = ' + str(self.current.speed.tilt))
        return True

    def findFirstNumeric(self, text):
        # print('Text to find numeric is:\n' + text)
        words = ' '.split(text)
        words = text.split(' ')
        print(words)
        for word in words:
            try:
                value = int(word)
                # print('word ' + word + ' is a number')
                return value
            except:
                # print('word ' + word + ' is not a number')
                pass

        return None

