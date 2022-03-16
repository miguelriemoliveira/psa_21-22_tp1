from abc import ABC, abstractmethod


class ClassAbstractHardware(ABC):

    def __init__(self):
        self.is_connected = False

    def connect(self, device):
        if self.is_connected:
            print('Cannot connect again to hardware!')
            return False

        self.is_connected = self._connect(device)
        print('Connected to hardware ' + str(self.is_connected))

    @abstractmethod
    def _connect(self, device):
        return

    def disconnect(self):
        if not self.is_connected:
            print('Already disconnected from hardware!')
            return False

        if self._disconnect():
            self.is_connected = False

    @abstractmethod
    def _disconnect(self):
        return

    def setData(self):
        if not self.is_connected:
            print('Cannot set data with hardware disconnected!')
            return False

        self._setData()

    @abstractmethod
    def _setData(self):
        return

    def getData(self):
        if not self.is_connected:
            print('Cannot get data with hardware disconnected!')
            return False

        return self._getData()

    @abstractmethod
    def _getData(self):
        return