import cv2
import time
import numpy as np
from pyardrone import ARDrone, at
print("import done")

drone = ARDrone()
drone.send(at.CONFIG('general:navdata_demo', True))
time.sleep(0.1)
drone.send(at.CONFIG("video:video_channel", 2))
time.sleep(0.1)
print("at done")

cam = cv2.VideoCapture('tcp://192.168.1.1:5555')

print("hoi")
while True:
    ret, img = cam.read()
    print("ret:", ret)
    if ret:
        cv2.imshow(" img", img)
        cv2.waitKey(1)

