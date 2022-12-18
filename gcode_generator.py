import math

from constants import HOME_X, HOME_Y, TRAVEL_SPEED, Z_UP, Z_DOWN, Z_SPEED, DRAW_SPEED

AUTO_HOME = 'G28'
TRAVEL = 'G0'
DRAW = 'G1'
WAIT = 'G4'

POINTS_PER_SECOND = 10


def move_straight(x0, y0, x1, y1, z0, z1, speed, cmd_type):
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2)
    steps = max(1, int(length * POINTS_PER_SECOND / speed))
    commands = []
    for i in range(steps):
        x = (x1 - x0) * i / steps + x0
        y = (y1 - y0) * i / steps + y0
        z = (z1 - z0) * i / steps + z0
        commands.append((cmd_type, x, y, z))
    return commands


def to_gcode(contours):
    res = []
    res.append((AUTO_HOME,))
    x = HOME_X
    y = HOME_Y

    for contour in contours:
        # travel to the start of the contour
        x0 = contour[-1][0]
        y0 = contour[-1][1]
        res.extend(move_straight(x, y, x0, y0, Z_UP, Z_UP, TRAVEL_SPEED, TRAVEL))
        x, y = x0, y0

        # drop the pen
        res.extend(move_straight(x, y, x, y, Z_UP, Z_DOWN, Z_SPEED, TRAVEL))
        res.append((WAIT, 500))

        # draw each line in the contour
        for i in range(len(contour)):
            x1, y1 = contour[i]
            res.extend(move_straight(x, y, x1, y1, Z_DOWN, Z_DOWN, DRAW_SPEED, DRAW))
            x, y = x1, y1

        res.append((WAIT, 500))

        # lift the pen
        res.extend(move_straight(x, y, x, y, Z_DOWN, Z_UP, Z_SPEED, TRAVEL))

    res.append((WAIT, 1000))
    res.append((AUTO_HOME,))
    return res

