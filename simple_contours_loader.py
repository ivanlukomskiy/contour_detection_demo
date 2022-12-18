import cv2
import numpy as np

from constants import SHEET_WIDTH, SHEET_HEIGHT
from gcode_generator import to_gcode


def get_contours(img):
    contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0][:-1]

    res = []
    for polyline in contours:
        points = []
        for point in polyline:
            points.append([int(point[0][0]), SHEET_HEIGHT - int(point[0][1])])
        res.append(points)
    return res


def fit_to_sheet(img):
    width = img.shape[1]
    height = img.shape[0]
    y_gap = 0
    x_gap = 0
    if width / height > SHEET_WIDTH / SHEET_HEIGHT:
        # fit by width
        k = SHEET_WIDTH / width
        y_gap = int((SHEET_HEIGHT - height * k) / 2)
    else:
        # fit by height
        k = SHEET_HEIGHT / height
        x_gap = int((SHEET_WIDTH - width * k) / 2)

    img = cv2.resize(img, (int(k * width), int(k * height)), interpolation=cv2.INTER_AREA)

    sheet = np.ones((SHEET_HEIGHT, SHEET_WIDTH, 3), np.uint8)
    sheet[y_gap:y_gap+img.shape[0], x_gap:x_gap+img.shape[1]] = img

    return sheet


def read_contours(filename):
    img = cv2.imread(filename)
    img = fit_to_sheet(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    return get_contours(img)


if __name__ == '__main__':
    img = cv2.imread('gamepad.jpeg')
    img = fit_to_sheet(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    contours = get_contours(img)
    gcode = to_gcode(contours)
    print(gcode)
    print(len(gcode))
    # contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0][:-1]
    # img[:] = 255
    # cv2.drawContours(img, contours, -1, (0, 0, 0), 1)
    # cv2.imshow('image', img)
    # cv2.waitKey(500000)
    # cv2.destroyAllWindows()
