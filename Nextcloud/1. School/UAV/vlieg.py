import pyqtgraph as pg
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from pyardrone import ARDrone, at


import cv2

print("hallotjes")

def init():
    uav = ARDrone()
    uav.navdata_ready.wait()

    print("ready2")
    return uav

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

drone.hover()
print("hover")
time.sleep(3)

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
