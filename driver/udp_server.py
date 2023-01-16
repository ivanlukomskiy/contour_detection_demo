import select
import socket
import struct
import traceback
from adafruit_servokit import ServoKit

UDP_IP = "0.0.0.0"
UDP_PORT = 5005
kit = ServoKit(channels=16, address=0x41)
shoulder_offset = 90
elbow_offset = 0

class UdpController:
    sock = None

    def __init__(self):
        print("Listening for UDP connections on {}:{}".format(UDP_IP, UDP_PORT))

    def udp_loop(self):
        while 1:
            ready = select.select([self.sock], [], [], 0.5)
            if ready[0]:
                try:
                    data, addr = self.sock.recvfrom(1024)
                    shoulder_angle, elbow_angle, wrist_angle = struct.unpack('ddd', data)
                    print("Angles received: {}, {}, {}".format(shoulder_angle, elbow_angle, wrist_angle))

                    # todo apply angles
                    kit.servo[0].angle = 180-max(min(shoulder_angle+shoulder_offset, 180), 0)
                    kit.servo[1].angle = max(min(elbow_angle+elbow_offset, 180), 0)
                    kit.servo[2].angle = wrist_angle
                except:
                    print("Failed to handle message", traceback.format_exc())

    def startup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.udp_loop()


control = UdpController()
control.startup()
