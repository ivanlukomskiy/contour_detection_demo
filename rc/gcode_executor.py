import math
from collections import Generator

from gcodeparser import GcodeLine

from constants import HOME_X, HOME_Y, Z_UP
from gcode_generator import AUTO_HOME, TRAVEL, DRAW, WAIT

POINTS_PER_SECOND = 10


def move_straight(x0, x1, y0, y1, z0, z1, speed):
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2)
    steps = max(1, int(length * POINTS_PER_SECOND / speed * 60))
    for i in range(steps):
        x = (x1 - x0) * (i + 1) / steps + x0
        y = (y1 - y0) * (i + 1) / steps + y0
        z = (z1 - z0) * (i + 1) / steps + z0
        yield x, y, z


class Executor:
    x = HOME_X
    y = HOME_Y
    z = Z_UP

    def __init__(self, target, play_speed=1):
        self.target = target
        self.play_speed = play_speed

    def execute(self, gcode: Generator[GcodeLine]):
        for cmd in gcode:
            if cmd.command == AUTO_HOME:
                self.target.apply(self.x, self.y, Z_UP)
                self.target.wait(int(500 / self.play_speed))
                self.target.apply(HOME_X, HOME_Y, Z_UP)
                self.target.wait(int(100000 / self.play_speed))
                self.x = HOME_X
                self.y = HOME_Y
                self.z = Z_UP

            elif cmd.command == TRAVEL or cmd.command == DRAW:
                x = cmd.params['X'] if 'X' in cmd.params else self.x
                y = cmd.params['Y'] if 'Y' in cmd.params else self.y
                z = cmd.params['Z'] if 'Z' in cmd.params else self.z
                speed = cmd.params['F']
                for x, y, z in move_straight(self.x, x, self.y, y, self.z, z, speed):
                    self.target.apply(x, y, z)
                    self.target.wait(int(1000 / POINTS_PER_SECOND / self.play_speed))
                self.x = x
                self.y = y
                self.z = z

            elif cmd.command == WAIT:
                duration = cmd.params['P']
                self.target.wait(int(duration / self.play_speed))
