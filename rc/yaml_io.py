import yaml


def load_profile(name):
    with open(f"profiles/{name}.yaml", "r") as stream:
        return yaml.safe_load(stream)


def save_profile(name, profile):
    with open(f"profiles/{name}.yaml", "w") as file:
        profile = {k: float(v) for k, v in profile.items()}
        yaml.dump(profile, file)


def save_calibration_points(name, data):
    with open(f"measurements/{name}.yaml", "w") as file:
        yaml.dump(data, file)


def load_calibration_points(name):
    with open(f"measurements/{name}.yaml", "r") as stream:
        return yaml.safe_load(stream)