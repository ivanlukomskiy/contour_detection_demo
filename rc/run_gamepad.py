from rc.gamepad import GamepadInput
from rc.target_simulator import SimTarget

if __name__ == '__main__':
    input = GamepadInput(SimTarget(None))
    input.startup()
