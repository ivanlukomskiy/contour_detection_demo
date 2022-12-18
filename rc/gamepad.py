import math

import pygame

SENDING_PERIOD_SEC = 0.1
JOYSTICK_THRESHOLD = 0.1
HORIZONTAL_SPEED_MAX = 50  # mm / s
VERTICAL_SPEED_MAX = 1  # mm / s
DELAY = 20


def axis_to_delta(axis, max_speed):
    if abs(axis) <= JOYSTICK_THRESHOLD:
        return 0
    normalized_axis = (abs(axis) - JOYSTICK_THRESHOLD) / (1 - JOYSTICK_THRESHOLD)
    unsigned_delta = normalized_axis * max_speed * DELAY / 1000
    signed_delta = math.copysign(unsigned_delta, axis)
    return signed_delta


class GamepadInput:
    x = 0
    y = 90
    z = 0

    def __init__(self, target):
        pygame.init()
        self.j = pygame.joystick.Joystick(0)
        self.target = target

    def events_handling_loop(self):
        while 1:
            pygame.event.pump()
            self.x += axis_to_delta(self.j.get_axis(2), HORIZONTAL_SPEED_MAX)
            self.y -= axis_to_delta(self.j.get_axis(3), HORIZONTAL_SPEED_MAX)
            self.z -= axis_to_delta(self.j.get_axis(1), VERTICAL_SPEED_MAX)
            self.z = min(1, self.z)
            self.z = max(0, self.z)
            self.target.apply(self.x, self.y, self.z)
            self.target.wait(DELAY)

    def startup(self):
        self.events_handling_loop()
