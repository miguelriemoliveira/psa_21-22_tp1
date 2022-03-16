import cv2
import pygame

from ClassAbstractHardware import ClassAbstractHardware

class ClassGamePad(ClassAbstractHardware):

    def __init__(self):
        super().__init__() # call super class constructor
        self.joystick = None
        self.axis0 = None
        self.axis1 = None

    def _connect(self, device):
        pygame.init()  # TODO find out if the pygame.init is really needed
        pygame.joystick.init()  # Initialize the joysticks

        joystick_count = pygame.joystick.get_count()
        print('Found ' + str(joystick_count) + ' joysticks.')

        if joystick_count < 1:
            print('No joysticks found. Cannot connect')
            return False

        self.joystick = pygame.joystick.Joystick(device)
        joystick_name = self.joystick.get_name()
        print('Connected to joystick named ' + joystick_name)
        return True

    def _disconnect(self):
        pygame.quit()
        return True

    def _setData(self):
        print('Nothing to write to game pad!')
        return False

    def _getData(self):
        self.axis0 = self.joystick.get_axis(0)
        self.axis1 = self.joystick.get_axis(1)
        pygame.event.pump()
        return True