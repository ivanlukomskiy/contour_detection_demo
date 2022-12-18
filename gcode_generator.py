from gcodeparser import GcodeLine

from constants import TRAVEL_SPEED, Z_UP, Z_DOWN, Z_SPEED, DRAW_SPEED

AUTO_HOME = ('G', 28)
TRAVEL = ('G', 0)
DRAW = ('G', 1)
WAIT = ('G', 4)


def to_gcode(contours):
    yield GcodeLine(('G', 28), {}, 'Auto home')

    for contour in contours:
        x, y = contour[-1][0], contour[-1][1]
        yield GcodeLine(TRAVEL, {'X': x, 'Y': y, 'F': TRAVEL_SPEED}, 'Travel to the start of next contour')

        yield GcodeLine(TRAVEL, {'Z': Z_DOWN, 'F': Z_SPEED}, 'Drop the pen')
        yield GcodeLine(WAIT, {'P': 500}, 'Delay')

        for i in range(len(contour)):
            x, y = contour[i]
            yield GcodeLine(DRAW, {'X': x, 'Y': y, 'F': DRAW_SPEED}, 'Draw segment')

        yield GcodeLine(WAIT, {'P': 500}, 'Delay')

        yield GcodeLine(TRAVEL, {'Z': Z_UP, 'F': Z_SPEED}, 'Lift the pen')

    yield GcodeLine(('G', 28), {}, 'Auto home')
    yield GcodeLine(WAIT, {'P': 3000}, 'Final delay')
