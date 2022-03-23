import pathlib
import tkinter as tk
import tkinter.ttk as ttk

import cv2
import pygubu

from PIL import Image
from PIL import ImageTk

from ClassGamePad import ClassGamePad
from ClassPTU import ClassPTU
from ClassCamera import ClassCamera

PROJECT_PATH = './'
PROJECT_UI = './MyApp.ui'


class ClassMyApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # main window
        self.main_window = builder.get_object('toplevelMain', master)
        self.main_window.resizable(width=False, height=False)
        self.main_window.bind('q', self.callbackCommandExit)
        self.main_window.bind('g', self.callbackGamePadConnect)
        self.main_window.bind('p', self.callbackPTUConnect)
        self.main_window.bind('c', self.callbackCameraConnect)

        # game pad window
        self.game_pad_window = builder.get_object('toplevelGamePad')
        self.game_pad_window.resizable(width=False, height=False)
        self.game_pad_window.bind('q', self.callbackCommandExit)
        self.game_pad_window.bind('g', self.callbackGamePadConnect)
        self.game_pad_window.bind('p', self.callbackPTUConnect)
        self.game_pad_window.bind('c', self.callbackCameraConnect)
        self.game_pad_window.withdraw()

        # ptu window
        self.ptu_window = builder.get_object('toplevelPTU')
        self.ptu_window.resizable(width=False, height=False)
        self.ptu_window.bind('q', self.callbackCommandExit)
        self.ptu_window.bind('g', self.callbackGamePadConnect)
        self.ptu_window.bind('p', self.callbackPTUConnect)
        self.ptu_window.bind('c', self.callbackCameraConnect)
        self.ptu_window.withdraw()

        # camera window
        self.camera_window = builder.get_object('toplevelCamera')
        self.camera_window.resizable(width=False, height=False)
        self.camera_window.bind('q', self.callbackCommandExit)
        self.camera_window.bind('g', self.callbackGamePadConnect)
        self.camera_window.bind('p', self.callbackPTUConnect)
        self.camera_window.bind('c', self.callbackCameraConnect)
        self.camera_window.withdraw()

        builder.connect_callbacks(self)

        # instantiote hardware communication classes
        self.game_pad = ClassGamePad()
        self.ptu = ClassPTU()
        self.ptu.goal.position.pan = 5000
        self.ptu.goal.position.tilt = 400
        self.camera = ClassCamera()

    # Main window callbacks
    def callbackCommandExit(self, key=None):
        print('Exiting ...')
        exit(0)

    # Camera callbacks
    def callbackCameraConnect(self, key=None):
        self.camera_window.deiconify()
        self.camera.connect(4)
        self.callbackCameraTimer()

    def callbackCameraDisconnect(self):
        self.camera_window.withdraw()
        self.camera.disconnect()

    def callbackCameraTimer(self):

        if not self.camera.getData():  # get new image from camera:
            return

        # OpenCV represents images in BGR order; however PIL
        # represents images in RGB order, so we need to swap
        # the channels, then convert to PIL and ImageTk format
        image = cv2.cvtColor(self.camera.image, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        # if the panel is not None, we need to initialize it
        panel = self.builder.get_object('labelImagePannel')
        panel.configure(image=image)
        panel.image = image

        # call this function after x milliseconds
        self.camera_window.after(200, self.callbackCameraTimer)
        # print('running game_pad timer')

    # PTU callbacks
    def callbackPTUConnect(self, key=None):
        self.ptu_window.deiconify()
        self.ptu.connect('/dev/ttyUSB0')
        self.callbackPTUTimer()

    def callbackPTUDisconnect(self):
        self.ptu_window.withdraw()
        self.ptu.disconnect()

    def callbackPTUTimer(self):

        self.ptu.setData()
        self.ptu.getData()

        self.builder.get_variable('entryPTUPanMonitorText').set(str(self.ptu.current.position.pan))
        self.builder.get_variable('entryPTUTiltMonitorText').set(str(self.ptu.current.position.tilt))

        self.builder.get_variable('entryPTUPanGoalMonitorText').set(str(self.ptu.goal.position.pan))
        self.builder.get_variable('entryPTUTiltGoalMonitorText').set(str(self.ptu.goal.position.tilt))

        # call this function after x milliseconds
        self.ptu_window.after(200, self.callbackPTUTimer)
        # print('running game_pad timer')

    def callbackScalePTUPanManualControl(self, value):
        value = int(float(value))
        self.ptu.goal.position.pan = value

    def callbackScalePTUTiltManualControl(self, value):
        value = int(float(value))
        self.ptu.goal.position.tilt = value

    # Game pad callbacks
    def callbackGamePadConnect(self, key=None):
        self.game_pad_window.deiconify()
        self.game_pad.connect(0)
        self.callbackGamePadTimer()

    def callbackGamePadDisconnect(self):
        self.game_pad_window.withdraw()
        self.game_pad.disconnect()

    def callbackGamePadTimer(self):

        if self.game_pad.getData():
            print('Axis0=' + str(self.game_pad.axis0) + '; Axis1=' + str(self.game_pad.axis1))
            formatted_axis0 = round(self.game_pad.axis0 * 100)/100
            formatted_axis1 = round(self.game_pad.axis1 * 100)/100
            self.builder.get_variable('entryAxis0TextVariable').set(formatted_axis0)
            self.builder.get_variable('entryAxis1TextVariable').set(formatted_axis1)


        # axis 0 set goal
        factor = 250
        if abs(self.game_pad.axis0) > 0.2:
            self.ptu.goal.position.pan += factor * self.game_pad.axis0
            self.ptu.goal.position.pan = min(8000, self.ptu.goal.position.pan)
            self.ptu.goal.position.pan = max(-8000, self.ptu.goal.position.pan)
            self.ptu.goal.position.pan = int(self.ptu.goal.position.pan)

        if abs(self.game_pad.axis1) > 0.2:
            self.ptu.goal.position.tilt += factor * self.game_pad.axis1
            self.ptu.goal.position.tilt = min(3000, self.ptu.goal.position.tilt)
            self.ptu.goal.position.tilt = max(-1500, self.ptu.goal.position.tilt)
            self.ptu.goal.position.tilt = int(self.ptu.goal.position.tilt)



        # call this function after x milliseconds
        self.game_pad_window.after(100, self.callbackGamePadTimer)
        # print('running game_pad timer')

    def run(self):
        self.main_window.mainloop()
