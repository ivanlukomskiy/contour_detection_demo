import math

import numdifftools as nd
import numpy as np
import yaml

from rc.geometry import angles_to_coords


def load_profile(name):
    with open(f"calibration_profile_{name}.yaml", "r") as stream:
        return yaml.safe_load(stream)


def save_profile(name, profile):
    with open(f"calibration_profile_{name}.yaml", "w") as file:
        yaml.dump(profile, file)


def save_calibration_points(name, data):
    with open(f"measurements_{name}.yaml", "w") as file:
        yaml.dump(data, file)


def load_calibration_points(name):
    with open(f"measurements_{name}.yaml", "r") as stream:
        return yaml.safe_load(stream)


def diff_function(calibration_points, profile):
    total_diff = 0
    for points in calibration_points['points']:
        x0, y0 = angles_to_coords(points['a'], points['b'], profile)
        total_diff += math.dist([x0, y0], [points['x'], points['y']]) ** 2
    return total_diff


LINEAR_WEIGHT = 8
ANGLE_WEIGHT = 0.8
ANGLE_MULTIPLIER_WEIGHT = 1

PARAM_WEIGHTS = {
    'upper_arm_length': LINEAR_WEIGHT,
    'upper_arm_angle_offset': ANGLE_WEIGHT,
    'upper_arm_angle_multiplier': ANGLE_MULTIPLIER_WEIGHT,
    'forearm_length': LINEAR_WEIGHT,
    'forearm_arm_angle_offset': ANGLE_WEIGHT,
    'forearm_arm_angle_multiplier': ANGLE_MULTIPLIER_WEIGHT,
    'sheet_distance': LINEAR_WEIGHT,
}

if __name__ == '__main__':
    ideal = load_profile('ideal')
    profile = load_profile('start')
    calibration_points = load_calibration_points('ideal')
    params = list(profile.keys())


    def _diff_function(params_vector):
        # print(f"> {params_vector}")
        _profile = {}
        for i, param in enumerate(params):
            _profile[param] = params_vector[i]
        return diff_function(calibration_points, _profile)


    def get_params(vector):
        res = {}
        for i, param in enumerate(params):
            res[param] = vector[i]
        return res


    vector = []
    for param in params:
        vector.append(profile[param])

    gradient_function = nd.Gradient(_diff_function)

    diff = _diff_function(vector)

    print(f"initial vector: {_diff_function(vector)}")

    for i in range(200):
        grad = gradient_function(vector)
        print(f"=== iteration {i} ===")
        print(f"gradient is {grad}")
        for param_index, param in enumerate(params):
            grad[param_index] = grad[param_index] * PARAM_WEIGHTS[param]
        print(f"fixed gradient is {grad}")

        diff = _diff_function(vector)
        print(f"diff is {diff}, tolerance {math.sqrt(diff)}")
        norm = np.linalg.norm(grad)
        print(f"norm is {norm}")
        force = (diff / 5) ** 2
        force = min(3., force)
        print(f"force is {force}")
        change = - force * grad / norm
        for param_index, param in enumerate(params):
            print(f"    {param:>30} {float(vector[param_index]):.2f} , delta {float(change[param_index]):.2f}" +
                  f" , ideal {ideal[param] - vector[param_index]}")
        vector += change
