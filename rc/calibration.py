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
        profile = {k: float(v) for k, v in profile.items()}
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


def get_weights(linear_weight, angle_weight):
    return {
        'upper_arm_length': linear_weight,
        'upper_arm_angle_offset': angle_weight,
        'forearm_length': linear_weight,
        'forearm_arm_angle_offset': angle_weight,
        'sheet_distance': linear_weight,
    }

DEFAULT_WEIGHTS = get_weights(8, 0.8)


def calculate_calibrations(approximation, iterations, output_calibration_name=None, weights=None,
                           speed_factor=0.2, max_speed=3., speed_power=2.):
    if weights is None:
        weights = DEFAULT_WEIGHTS

    profile = load_profile(approximation)
    calibration_points = load_calibration_points('ideal')
    params = list(profile.keys())

    def _to_profile(params_vector):
        _profile = {}
        for i, param in enumerate(params):
            _profile[param] = params_vector[i]
        return _profile

    def _diff_function(params_vector):
        return diff_function(calibration_points, _to_profile(params_vector))

    vector = []
    for param in params:
        vector.append(profile[param])

    gradient_function = nd.Gradient(_diff_function)

    # print(f"initial vector: {_diff_function(vector)}")

    diff = 0

    for i in range(iterations):
        grad = gradient_function(vector)
        # print(f"=== iteration {i} ===")
        # print(f"gradient is {grad}")
        for param_index, param in enumerate(params):
            grad[param_index] = grad[param_index] * weights[param]
        # print(f"fixed gradient is {grad}")

        diff = _diff_function(vector)
        # print(f"diff is {diff}, tolerance {math.sqrt(diff)}")
        norm = np.linalg.norm(grad)
        # print(f"norm is {norm}")
        speed_factor = (diff * speed_factor) ** speed_power
        speed_factor = min(max_speed, speed_factor)
        # print(f"force is {speed_factor}")
        change = - speed_factor * grad / norm
        # for param_index, param in enumerate(params):
        #     print(f"    {param:>30} {float(vector[param_index]):.2f} , delta {float(change[param_index]):.2f}")
        vector += change

    tolerance = math.sqrt(diff)

    if output_calibration_name:
        profile = _to_profile(vector)
        profile['tolerance'] = tolerance
        save_profile(output_calibration_name, profile)

    return tolerance


if __name__ == '__main__':
    min_tolerance = 1000
    best_params = None

    with open('results.txt', 'a') as file:

        for linear_weight in [2, 4, 6, 8, 10, 14, 20]:
            for speed_factor in [0.1, 0.15, 0.2, 0.28, 0.4]:
                for max_speed in [2, 3, 6, 10, 16]:
                    for speed_power in [1, 1.5, 2, 2.4, 3]:
                        for angle_weight in [0.4, 0.6, 0.8, 1., 1.5, 2, 2.5]:
                            tolerance = calculate_calibrations('start', 500, 'out',
                                                               get_weights(linear_weight, angle_weight),
                                                               speed_factor=speed_factor, max_speed=max_speed)
                            params = linear_weight, speed_factor, max_speed, speed_power, angle_weight
                            if tolerance < min_tolerance:
                                min_tolerance = tolerance
                                best_params = params
                            print(f'tolerance for {params} is {tolerance}')
                            file.write(f'{params}, {tolerance}\n')

        print('best params: ', best_params)
