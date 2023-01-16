import math

from rc.constants import SHEET_WIDTH, MIN_DISTANCE


def sheet_coords_to_angles(x, y, profile, safe=True):
    x = x - SHEET_WIDTH / 2
    y = y + profile['sheet_distance']
    l3 = math.sqrt(x ** 2 + y ** 2)

    if not safe and profile['forearm_length'] + profile['upper_arm_length'] < l3:
        raise RuntimeError("unreachable point")

    l3_fixed = min(l3, profile['forearm_length'] + profile['upper_arm_length'])
    l3_fixed = max(l3_fixed, MIN_DISTANCE)
    x = x * l3_fixed / l3
    y = y * l3_fixed / l3

    b_cos = (profile['forearm_length'] ** 2 + profile['upper_arm_length'] ** 2 - l3_fixed ** 2) \
            / 2 / profile['forearm_length'] / profile['upper_arm_length']
    b_cos = max(-1, min(1, b_cos))

    b = math.degrees(math.acos(b_cos))

    a2 = math.atan2(x, y)
    a1_cos = (profile['upper_arm_length'] ** 2 + l3_fixed ** 2 - profile['forearm_length'] ** 2) \
             / 2 / profile['upper_arm_length'] / l3_fixed
    a1_cos = max(-1, min(1, a1_cos))
    a1 = math.acos(a1_cos)

    a = math.degrees(a1 + a2)
    return a + profile['upper_arm_angle_offset'], b + profile['forearm_arm_angle_offset']


def angles_to_coords(a, b, profile):
    a = a - profile['upper_arm_angle_offset']
    b = b - profile['forearm_arm_angle_offset']
    t = math.radians(180 - a - b)
    a = math.radians(a)
    x = profile['upper_arm_length'] * math.sin(a) - profile['forearm_length'] * math.sin(t)
    y = profile['upper_arm_length'] * math.cos(a) + profile['forearm_length'] * math.cos(t)
    y -= profile['sheet_distance']
    x += SHEET_WIDTH / 2
    return x, y
