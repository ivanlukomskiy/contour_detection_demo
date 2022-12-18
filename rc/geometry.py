import math

from rc.constants import SHEET_WIDTH, SHEET_DISTANCE, UPPER_ARM_LENGTH, FOREARM_LENGTH, MIN_DISTANCE


def sheet_coords_to_angles(x, y):
    x = x - SHEET_WIDTH / 2
    y = y + SHEET_DISTANCE
    l3 = math.sqrt(x ** 2 + y ** 2)

    l3_fixed = min(l3, FOREARM_LENGTH + UPPER_ARM_LENGTH)
    l3_fixed = max(l3_fixed, MIN_DISTANCE)
    x = x * l3_fixed / l3
    y = y * l3_fixed / l3

    b_cos = (FOREARM_LENGTH ** 2 + UPPER_ARM_LENGTH ** 2 - l3_fixed ** 2) / 2 / FOREARM_LENGTH / UPPER_ARM_LENGTH

    b = math.degrees(math.acos(b_cos))

    a2 = math.atan2(x, y)
    a1_cos = (UPPER_ARM_LENGTH ** 2 + l3_fixed ** 2 - FOREARM_LENGTH ** 2) / 2 / UPPER_ARM_LENGTH / l3_fixed
    a1 = math.acos(a1_cos)

    a = math.degrees(a1 + a2)

    return a, b
