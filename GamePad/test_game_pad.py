#!/usr/bin/env python3
import time

import pygame

# -------------------------
# Initialization
# -------------------------

# pygame.init()  # TODO find out if the pygame.init is really needed
pygame.joystick.init()  # Initialize the joysticks

joystick_count = pygame.joystick.get_count()
print('Found ' + str(joystick_count) + ' joysticks.')

if joystick_count < 1:
    print('No joysticks found. Terminating.')
    exit(0)

joystick = pygame.joystick.Joystick(0)
joystick_name = joystick.get_name()

print('Connected to joystick named ' + joystick_name)

# -------------------------
# Execution in cycle
# -------------------------

while True:
    # TODO why is this not working ...
    # for event in pygame.event.get():  # User did something.
    #     if event.type == pygame.JOYBUTTONDOWN:
    #         print("Joystick button down pressed.")
    #     elif event.type == pygame.JOYBUTTONUP:
    #         print("Joystick button up released.")

    joystick = pygame.joystick.Joystick(0)
    axis0 = joystick.get_axis(0)
    axis1 = joystick.get_axis(1)

    print('Axis0=' + str(axis0) + '; Axis1=' + str(axis1))
    time.sleep(0.1)

# -------------------------
# Termination
# -------------------------

pygame.quit()
