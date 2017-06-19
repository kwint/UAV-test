import cv2
import time
import numpy as np
from pyardrone import ARDrone, at
import threading

print("import done")


def droneMove():
    print('hoi')




moveData = 10
drone = 1
while True:
    tijd = time.time()
    movethread = threading.Thread(target=droneMove)
    movethread.start()
    print(time.time() - tijd)
#
# if not movethread.is_alive() and moveData.marker:
#     movethread = threading.Thread(target=droneMove, args=(moveData, drone))
#     movethread.start()
#     moveData.marker = False
