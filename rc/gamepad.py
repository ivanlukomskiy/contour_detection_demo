import math
from datetime import datetime

import pygame

from rc.geometry import sheet_coords_to_angles
from rc.yaml_io import save_calibration_points

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
    calibration_points = []

    def __init__(self, target, simulator, profile):
        self.profile = profile
        self.simulator = simulator
        pygame.init()
        self.j = pygame.joystick.Joystick(0)
        self.target = target

    def events_handling_loop(self):
        while 1:
            pygame.event.pump()
            events = pygame.event.get(eventtype=pygame.JOYBUTTONUP)
            for event in events:
                if event.button == 0:  # B
                    a, b = sheet_coords_to_angles(self.x, self.y, self.profile)
                    print(f"Saving calibration point, a={a} deg, b={b} deg")
                    try:
                        print(f"x:")
                        x = float(input())
                        print(f"y:")
                        y = float(input())
                        point = {'x': x, 'y': y, 'a': a, 'b': b}
                        self.calibration_points.append(point)
                        print(f'Calibration point saved {point}')
                    except:
                        print("Invalid input")
                if event.button == 1:
                    if not self.calibration_points:
                        print("No points to save\n")
                        continue
                    name = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    save_calibration_points(name, {'points': self.calibration_points})
                    self.calibration_points.clear()
                    print(f"Calibration points saved to file {name}")
                if event.button == 2:
                    print("Exit")
                    return

            self.x += axis_to_delta(self.j.get_axis(2), HORIZONTAL_SPEED_MAX)
            self.y -= axis_to_delta(self.j.get_axis(3), HORIZONTAL_SPEED_MAX)
            self.z -= axis_to_delta(self.j.get_axis(1), VERTICAL_SPEED_MAX)
            self.z = min(1, self.z)
            self.z = max(0, self.z)
            self.simulator.apply(self.x, self.y, self.z)
            self.target.apply(self.x, self.y, self.z)
            self.simulator.wait(DELAY)

    def startup(self):
        self.events_handling_loop()
