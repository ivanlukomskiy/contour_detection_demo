from gcode_executor import Executor
from gcode_generator import to_gcode
from sim_target import SimTarget
from simple_contours_loader import read_contours

if __name__ == '__main__':
    contours = read_contours('gamepad.jpeg')
    gcode = to_gcode(contours)

    executor = Executor(SimTarget(contours), play_speed=8)

    executor.execute(gcode)

    gcode = to_gcode(contours)
    with open('plan.gcode', 'w') as f:
        for cmd in gcode:
            f.write(cmd.gcode_str + '\n')

