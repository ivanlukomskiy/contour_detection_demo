import math
import time

import cv2
import numpy as np

from constants import VIEW_WIDTH, VIEW_HEIGHT, VIEW_SCALE, UPPER_ARM_LENGTH, ARM_THICKNESS, \
    FOREARM_LENGTH, SHEET_DISTANCE, SHEET_WIDTH, SHEET_HEIGHT, SHEET_COLOR, MIN_DISTANCE, \
    CONTOUR_COLOR, CONTOUR_THICKNESS, HOME_X, Z_UP, HOME_Y
from gcode_generator import to_gcode, POINTS_PER_SECOND, TRAVEL, DRAW, WAIT
from simple_contours_loader import read_contours

# util constants
X0 = int(VIEW_WIDTH / 2)
Y0 = int(VIEW_HEIGHT / 6)


def line(image, x0, y0, x1, y1, thickness=3, color=None):
    cv2.line(
        image,
        (int(x0 * VIEW_SCALE + X0), int(VIEW_HEIGHT - y0 * VIEW_SCALE - Y0)),
        (int(x1 * VIEW_SCALE + X0), int(VIEW_HEIGHT - y1 * VIEW_SCALE - Y0)),
        color or (255, 0, 0),
        thickness
    )


def draw_arm(image, _shoulder_angle, _elbow_angle, color):
    shoulder_angle_rad = math.radians(_shoulder_angle)
    elbow_x = UPPER_ARM_LENGTH * math.sin(shoulder_angle_rad)
    elbow_y = UPPER_ARM_LENGTH * math.cos(shoulder_angle_rad)
    line(image, 0, 0, elbow_x, elbow_y, ARM_THICKNESS, color)

    forearm_angle_rad = math.pi - shoulder_angle_rad - math.radians(_elbow_angle)
    wrist_x = elbow_x - FOREARM_LENGTH * math.sin(forearm_angle_rad)
    wrist_y = elbow_y + FOREARM_LENGTH * math.cos(forearm_angle_rad)
    line(image, elbow_x, elbow_y, wrist_x, wrist_y, ARM_THICKNESS, color)


def sheet_coords_to_global(x, y):
    return -SHEET_WIDTH / 2 + x, SHEET_DISTANCE + y


def draw_sheet(image):
    line(image, -SHEET_WIDTH / 2, SHEET_DISTANCE,
         SHEET_WIDTH / 2, SHEET_DISTANCE,
         3, SHEET_COLOR)
    line(image, SHEET_WIDTH / 2, SHEET_DISTANCE,
         SHEET_WIDTH / 2, SHEET_DISTANCE + SHEET_HEIGHT,
         3, SHEET_COLOR)
    line(image, SHEET_WIDTH / 2, SHEET_DISTANCE + SHEET_HEIGHT, -SHEET_WIDTH / 2,
         SHEET_DISTANCE + SHEET_HEIGHT,
         3, SHEET_COLOR)
    line(image, -SHEET_WIDTH / 2, SHEET_DISTANCE + SHEET_HEIGHT,
         -SHEET_WIDTH / 2, SHEET_DISTANCE,
         3, SHEET_COLOR)


def draw_contour_segment(img, coords0, coords1):
    x0, y0 = sheet_coords_to_global(coords0[0], coords0[1])
    x1, y1 = sheet_coords_to_global(coords1[0], coords1[1])
    line(img, x0, y0, x1, y1, CONTOUR_THICKNESS, CONTOUR_COLOR)


def draw_contour(img, contour):
    for i in range(len(contour) - 1):
        draw_contour_segment(img, contour[i], contour[i + 1])
    draw_contour_segment(img, contour[0], contour[-1])


def draw_contours(img, contours):
    for contour in contours:
        draw_contour(img, contour)


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


if __name__ == '__main__':
    contours = read_contours('gamepad.jpeg')
    gcode = to_gcode(contours)
    i = 0
    x = HOME_X
    y = HOME_Y
    z = Z_UP

    while True:
        img = np.zeros((VIEW_HEIGHT, VIEW_WIDTH, 3), np.uint8)

        instruction = gcode[i]
        if instruction[0] == TRAVEL or instruction[0] == DRAW:
            x = instruction[1]
            y = instruction[2]
            z = instruction[3]

        shoulder_angle, elbow_angle = sheet_coords_to_angles(x, y)
        # x y ok
        draw_sheet(img)
        draw_contours(img, contours)
        draw_arm(img, shoulder_angle, elbow_angle, (0, int(255 * z), int(255 * (1 - z))))
        cv2.imshow('image', img)
        if cv2.waitKey(int(100 / POINTS_PER_SECOND)) & 0xFF == ord('q'):
            break

        if instruction[0] == WAIT:
            time.sleep(instruction[1] / 1000)

        i += 1
        i = i % len(gcode)

    cv2.destroyAllWindows()
