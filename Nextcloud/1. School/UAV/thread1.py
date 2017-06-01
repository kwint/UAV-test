import time
import thread3
from pyardrone import ARDrone, at

import cv2


def init():
    drone = ARDrone()
    drone.send(at.CONFIG('general:navdata_demo', True))
    drone.emergency()
    print("send")
    return drone


cv2.namedWindow("hoi")
# Connect to drone and send some commands to it
drone = init()
#
drone.navdata_ready.wait()  # wait until NavData is ready
print("ready")
# Create new threads


drone.navdata_ready.wait()  # wait until NavData is ready

while not drone.state.fly_mask:
    drone.takeoff()
    print("Vlieg op!")
print("JA baas")

timeout = time.time() + 10
while True:
    drone.move(ccw=0.2)
    if time.time() > timeout:
        break

timeout = time.time() + 10
while True:
    drone.move(cw=0.2)
    if time.time() > timeout:
        break

print("klaar")
while drone.state.fly_mask:
    drone.land()
    print("ga landen maat")

print("doei")
