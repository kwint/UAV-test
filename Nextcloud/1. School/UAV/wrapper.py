import threading
from pyardrone import ARDrone, at
import time

import vlieg



class Besturing(threading.Thread):
    def __init__(self, threadID, drone):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.drone = drone

    def run(self):
        print("Starting ")
        vlieg.process(drone)
        print("Exiting ")

class Video(threading.Thread):
    def __init__(self, threadID, drone):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.drone = drone

    def run(self):
        print("Starting ")
        vlieg.process(drone)
        print("Exiting ")


def init():
    uav = ARDrone()
    print("ready to wait")
    uav.navdata_ready.wait()
    print("ready")
    uav.send(at.CONFIG('general:navdata_demo', True))
    time.sleep(0.1)
    print("send")
    while uav.state.emergency_mask:
        print("emergency")
        uav.send(at.REF(0b0100000000))
        time.sleep(1)
    print("ready1")
    return uav
drone = 1
# drone = init()

print("maak thread")
thread = Besturing(1, drone)
thread.start()

while True:
   time.sleep(0.5)