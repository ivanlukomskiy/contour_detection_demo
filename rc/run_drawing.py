from gcode_executor import Executor
from gcode_generator import to_gcode
from rc.target_simulator import SimTarget

from rc.target_udp import RcTarget
from rc.yaml_io import load_profile
from simple_contours_loader import read_contours

if __name__ == '__main__':
    contours = read_contours('assets/gamepad.jpeg')
    profile = load_profile('calibrated')

    gcode = to_gcode(contours)

    executor = Executor(SimTarget(contours, profile=profile), play_speed=8)
    # executor = Executor(RcTarget(), play_speed=8)

    executor.execute(gcode)

    gcode = to_gcode(contours)
    with open('../assets/plan.gcode', 'w') as f:
        for cmd in gcode:
            f.write(cmd.gcode_str + '\n')

