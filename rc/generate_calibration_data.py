import random

import numpy as np

from rc.calibration import load_profile, save_calibration_points
from rc.constants import SHEET_WIDTH, SHEET_HEIGHT
from rc.geometry import sheet_coords_to_angles

X_OFFSET = 50
Y_OFFSET = 50


def generate():
    x_grid, y_grid = np.mgrid[
                         X_OFFSET:SHEET_WIDTH - X_OFFSET + 1:(SHEET_WIDTH - 2 * X_OFFSET) / 3,
                         Y_OFFSET:SHEET_HEIGHT - Y_OFFSET + 1:(SHEET_HEIGHT - 2 * Y_OFFSET) / 3,
                     ]
    x, y = np.vstack([x_grid.ravel(), y_grid.ravel()])
    ideal_profile = load_profile('ideal')

    def to_angles(_x, _y):
        return sheet_coords_to_angles(_x, _y, ideal_profile, safe=False)

    f = np.vectorize(to_angles, otypes=(float, float))

    a, b = f(x, y)
    x += random.uniform(-5., 5.)
    y += random.uniform(-5., 5.)
    return np.dstack((x, y, a, b))[0]


if __name__ == '__main__':
    points = generate()
    res = {'points': []}
    for point in points:
        res['points'].append({
            'x': float(point[0]),
            'y': float(point[1]),
            'a': float(point[2]),
            'b': float(point[3]),
        })
    print(res)
    save_calibration_points('tolerance_10mm', res)
