from rc.gamepad import GamepadInput
from rc.target_simulator import SimTarget
from rc.target_udp import RcTarget

if __name__ == '__main__':
    input = GamepadInput(RcTarget(), SimTarget(None))
    input.startup()
