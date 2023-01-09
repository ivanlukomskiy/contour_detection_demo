import pygame

SENDING_PERIOD_SEC = 0.1
JOYSTICK_THRESHOLD = 0.1
HORIZONTAL_SPEED_MAX = 50  # mm / s
VERTICAL_SPEED_MAX = 1  # mm / s
DELAY = 10
HORIZONTAL_ACCELERATION = 0.05
MAX_SPEED = 0.4

class KeyboardInput:
    x = 0
    y = 90
    z = 0
    vx = 0
    vy = 0
    vz = 0
    calibration_points = []

    def __init__(self, simulator, profile):
        self.profile = profile
        self.simulator = simulator
        pygame.init()

    def events_handling_loop(self):
        while 1:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.vy += HORIZONTAL_ACCELERATION
            elif keys[pygame.K_s]:
                self.vy -= HORIZONTAL_ACCELERATION
            else:
                self.vy = 0

            if keys[pygame.K_a]:
                self.vx -= HORIZONTAL_ACCELERATION
            elif keys[pygame.K_d]:
                self.vx += HORIZONTAL_ACCELERATION
            else:
                self.vx = 0

            if abs(self.vx) > MAX_SPEED:
                self.vx = MAX_SPEED * self.vx / abs(self.vx)
            if abs(self.vy) > MAX_SPEED:
                self.vy = MAX_SPEED * self.vy / abs(self.vy)

            if keys[pygame.K_q]:
                return
            self.x += self.vx
            self.y += self.vy
            self.simulator.apply(self.x, self.y, self.z)
            self.simulator.wait(DELAY)

    def startup(self):
        self.events_handling_loop()
