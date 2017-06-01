import pyqtgraph as pg
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from pyardrone import ARDrone, at


import cv2

print("hallotjes")

def init():
    uav = ARDrone()
    print("ready to wait2")
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



def test():
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

    timeout = time.time() + 5
    while True:
        drone.move(forward=0.2)
        if time.time() > timeout:
            break

    timeout = time.time() + 5
    while True:
        drone.move(backward=0.2)
        if time.time() > timeout:
            break

    print("klaar")
    while drone.state.fly_mask:
        drone.land()
        print("ga landen maat")

    print("doei")
