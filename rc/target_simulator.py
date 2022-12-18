import math

import cv2
import numpy as np

from constants import VIEW_WIDTH, VIEW_HEIGHT, VIEW_SCALE, UPPER_ARM_LENGTH, ARM_THICKNESS, \
    FOREARM_LENGTH, SHEET_DISTANCE, SHEET_WIDTH, SHEET_HEIGHT, SHEET_COLOR, MIN_DISTANCE, \
    CONTOUR_COLOR, CONTOUR_THICKNESS
from rc.geometry import sheet_coords_to_angles

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


class SimTarget:
    def __init__(self, contours):
        self.contours = contours

    def apply(self, x, y, z):
        img = np.zeros((VIEW_HEIGHT, VIEW_WIDTH, 3), np.uint8)

        shoulder_angle, elbow_angle = sheet_coords_to_angles(x, y)
        draw_sheet(img)
        if self.contours:
            draw_contours(img, self.contours)
        color = (0, int(255 * z), int(255 * (1 - z)))
        print(f'{z} -> {color}')
        draw_arm(img, shoulder_angle, elbow_angle, color)

        cv2.imshow('image', img)

    def wait(self, milliseconds):
        cv2.waitKey(int(milliseconds))

    def stop(self):
        cv2.destroyAllWindows()
