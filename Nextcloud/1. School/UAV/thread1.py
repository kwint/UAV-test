
import threading
import time
import GetData
import thread3
from pyardrone import ARDrone, at
import pygame
import cv2

class GetNavData(threading.Thread):
    def __init__(self, threadID, drone):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.drone = drone

    def run(self):
        print("Starting ")
        GetData
        print("Exiting ")


class GetCameraFeed(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("Starting ")
        thread3.getvideo()
        print("Exiting ")


def init():
    drone = ARDrone()
    drone.send(at.CONFIG('general:navdata_demo', True))
    drone.send(at.REF(0b0100000000))
    print("send")
    return drone


cv2.namedWindow("hoi")
drone = 0
# Connect to drone and send some commands to it
# drone = init()
#
# drone.navdata_ready.wait()  # wait until NavData is ready
# print("ready")
# Create new threads
thread2 = GetNavData(1, drone)
# thread3 = GetCameraFeed(2)

# Start new Threads
thread2.start()
# thread3.start()

drone.navdata_ready.wait()  # wait until NavData is ready
while not drone.state.fly_mask:
    drone.takeoff()





print("Shutting down...")

print("Ok.")

