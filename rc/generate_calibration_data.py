import numpy as np

from rc.calibration import load_profile, save_calibration_points
from rc.geometry import sheet_coords_to_angles


def generate():
    x_grid, y_grid = np.mgrid[0:250 + 1:250 / 3, 0:135 + 1:135 / 3]
    x, y = np.vstack([x_grid.ravel(), y_grid.ravel()])
    ideal_profile = load_profile('ideal')

    def to_angles(_x, _y):
        return sheet_coords_to_angles(_x, _y, ideal_profile)

    f = np.vectorize(to_angles, otypes=(float, float))

    a, b = f(x, y)
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
    save_calibration_points('ideal', res)
