import math

from rc.constants import SHEET_WIDTH, SHEET_DISTANCE, UPPER_ARM_LENGTH, FOREARM_LENGTH, MIN_DISTANCE


def sheet_coords_to_angles(x, y):
    x = x - SHEET_WIDTH / 2
    y = y + SHEET_DISTANCE
    l3 = math.sqrt(x ** 2 + y ** 2)
    if l3 > FOREARM_LENGTH + UPPER_ARM_LENGTH:
        raise RuntimeError(f'Point is too far away: {l3}')

    if l3 < MIN_DISTANCE:
        raise RuntimeError(f'Point is too close: {l3}')

    b_cos = (FOREARM_LENGTH ** 2 + UPPER_ARM_LENGTH ** 2 - l3 ** 2) / 2 / FOREARM_LENGTH / UPPER_ARM_LENGTH
    if b_cos > 1 or b_cos < -1:
        raise RuntimeError('Unsolvable "b" position')  # should never happen

    b = math.degrees(math.acos(b_cos))

    a2 = math.atan2(x, y)
    a1_cos = (UPPER_ARM_LENGTH ** 2 + l3 ** 2 - FOREARM_LENGTH ** 2) / 2 / UPPER_ARM_LENGTH / l3
    if a1_cos > 1 or a1_cos < -1:
        raise RuntimeError('Unsolvable "a" position')  # should never happen
    a1 = math.acos(a1_cos)

    a = math.degrees(a1 + a2)

    return a, b
