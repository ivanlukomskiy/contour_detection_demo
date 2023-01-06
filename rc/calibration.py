import math

import numdifftools as nd
import numpy as np
import yaml

from rc.gamepad import GamepadInput
from rc.geometry import angles_to_coords
from rc.profiles import load_profile, load_calibration_points, save_profile
from rc.target_simulator import SimTarget
from rc.target_udp import RcTarget


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
                           speed_factor=0.01, max_speed=3., speed_power=.6):
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

    print(f"initial vector: {_diff_function(vector)}")

    diff = 0

    for i in range(iterations):
        grad = gradient_function(vector)
        print(f"=== iteration {i} ===")
        print(f"gradient is {grad}")
        for param_index, param in enumerate(params):
            grad[param_index] = grad[param_index] * weights[param]
        print(f"fixed gradient is {grad}")

        diff = _diff_function(vector)
        print(f"diff is {diff}, tolerance {math.sqrt(diff)}")
        norm = np.linalg.norm(grad)
        print(f"norm is {norm}")
        sf = (diff * speed_factor) ** speed_power
        sf = min(max_speed, sf)
        print(i, " diff: ",diff," sf: ", sf)
        print(f"force is {speed_factor}")
        change = - sf * grad / norm
        for param_index, param in enumerate(params):
            print(f"    {param:>30} {float(vector[param_index]):.2f} , diff {float(grad[param_index])} delta {float(change[param_index]):.2f}")

        vector += change

    tolerance = math.sqrt(diff)

    if output_calibration_name:
        profile = _to_profile(vector)
        profile['tolerance'] = tolerance
        save_profile(output_calibration_name, profile)

    return tolerance


if __name__ == '__main__':
    input = GamepadInput(RcTarget(), SimTarget(None))
    input.startup()
