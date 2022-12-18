import time
from threading import Thread

from inputs import get_gamepad

LEFT_THRESHOLD = -3000
RIGHT_THRESHOLD = 3000
LEFT_MAX = -32768
RIGHT_MAX = 32767
X_INPUT_CODE = 'ABS_RX'
Y_INPUT_CODE = 'ABS_RY'
X_CHANNEL = 1
Y_CHANNEL = 2

SENDING_PERIOD_SEC = 0.1


def position_to_percents(value):
    if LEFT_THRESHOLD < value < RIGHT_THRESHOLD:
        return 0
    if value < 0:
        return - value * 100 / LEFT_MAX
    return value * 100 / RIGHT_MAX


class GamepadInput:
    # current_x_value = 0
    # driver_x_value = 0
    # current_y_value = 0
    # driver_y_value = 0
    shoulder_angle = 0
    elbow_angle = 0
    wrist_angle = 0

    def __init__(self, target):
        self.target = target

    def events_handling_loop(self):
        while 1:
            events = get_gamepad()
            for event in events:
                if event.code == X_INPUT_CODE:
                    self.shoulder_angle = position_to_percents(event.state)
                elif event.code == Y_INPUT_CODE:
                    self.elbow_angle = position_to_percents(event.state)
            print(f'{self.shoulder_angle}\t\t{self.elbow_angle}\t\t{self.wrist_angle}')

    def rest_client_loop(self):
        while 1:
            time.sleep(SENDING_PERIOD_SEC)
            # self.target.apply(self.shoulder_angle, self.elbow_angle, self.wrist_angle)

    def startup(self):
        Thread(target=self.events_handling_loop).start()
        Thread(target=self.rest_client_loop()).start()
