import math

import numpy as np
import yaml
import numdifftools as nd

from rc.geometry import sheet_coords_to_angles, angles_to_coords


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
        # a, b = sheet_coords_to_angles(points['x'], points['y'], profile)
        # todo how do i compare the actual distance, not what was recorded in the measurement

        # what will we get if we blindly apply a and b to our current profile
        x0, y0 = angles_to_coords(points['a'], points['b'], profile)
        total_diff += math.dist([x0, y0], [points['x'], points['y']]) ** 2
        # total_diff += (a - points['a']) ** 2 + (b - points['b']) ** 2
    return total_diff


MAX_CHANGE = {
    'upper_arm_length': 1,
    'upper_arm_angle_offset': 1,
    'upper_arm_angle_multiplier': 1,
    'forearm_length': 1,
    'forearm_arm_angle_offset': 1,
    'forearm_arm_angle_multiplier': 1,
    'sheet_distance': 100,
}

if __name__ == '__main__':
    # profile = load_profile('ideal')
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
        diff = _diff_function(vector)
        print(f"diff is {diff}")
        norm = np.linalg.norm(grad)
        print(f"norm is {norm}")
        force = (diff / 3) ** 2
        force = min(3., force)
        print(f"force is {force}")
        change = - force * grad / norm
        for param_index, param in enumerate(params):
            print(f"    {param} = {vector[param_index]} , delta {change[param_index]}")
        vector += change

    # diff = diff_function(calibration_points, profile)
    # print(diff)
