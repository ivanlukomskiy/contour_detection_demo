from rc.keyboard import KeyboardInput
from rc.target_simulator import SimTarget
from rc.yaml_io import load_profile

if __name__ == '__main__':
    profile = load_profile('calibrated')
    input = KeyboardInput(SimTarget(None, profile), profile)
    input.startup()
