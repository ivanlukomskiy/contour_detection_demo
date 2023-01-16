import socket
import struct
import time

from constants import MAX_WRIST_ANGLE, MIN_WRIST_ANGLE
from rc.geometry import sheet_coords_to_angles

SERVER_IP = '10.81.2.201'
SERVER_PORT = 5005


class RcTarget:
    def __init__(self, profile):
        self.profile = profile
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def apply(self, x, y, z):
        shoulder_angle, elbow_angle = sheet_coords_to_angles(x, y, self.profile)
        wrist_angle = z * (MAX_WRIST_ANGLE - MIN_WRIST_ANGLE) + MIN_WRIST_ANGLE
        # print(f'sending {shoulder_angle} {elbow_angle} {wrist_angle}')
        self.sock.sendto(struct.pack('ddd', shoulder_angle, elbow_angle, wrist_angle),
                         (SERVER_IP, SERVER_PORT))

    def wait(self, milliseconds):
        time.sleep(milliseconds / 1000)
