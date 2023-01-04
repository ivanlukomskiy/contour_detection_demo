#
# import numdifftools as nd
#
# def f1(i):
#     return i[0] ** 2 + i[1] ** 2
# grad = nd.Gradient(f1)([1, 33])
# print(grad)
import yaml


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
