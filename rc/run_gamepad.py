from rc.gamepad import GamepadInput
from rc.target_simulator import SimTarget
from rc.target_udp import RcTarget
from rc.yaml_io import load_profile

if __name__ == '__main__':
    profile = load_profile('ideal')
    input = GamepadInput(RcTarget(profile), SimTarget(None))
    input.startup()
