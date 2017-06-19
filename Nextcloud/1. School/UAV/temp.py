import cv2
import time
import numpy as np
from pyardrone import ARDrone, at
print("import done")

cam = cv2.VideoCapture('tcp://192.168.1.1:5555')

drone = ARDrone()
drone.send(at.CONFIG('general:navdata_demo', True))
time.sleep(0.1)
drone.send(at.CONFIG("video:video_channel", 1))
time.sleep(0.1)
print("at done")

sleep = 15

timeout = time.time() + sleep
previous_time = time.time()

print("hoi")
while True:
    ret, img = cam.read()
    current_time = time.time()-previous_time
    print("ret:", ret, '/time:', current_time)
    if ret:
        cv2.imshow(" img", img)
        cv2.waitKey(1)
    if time.time() > timeout:
        break

print("switch")
drone.send(at.CONFIG("video:video_channel", 0))
previous_time = time.time()
timeout = time.time() + sleep

while True:
    ret, img = cam.read()
    current_time = time.time()-previous_time
    print("ret:", ret, '/time:', current_time)
    if ret:
        cv2.imshow(" img", img)
        cv2.waitKey(1)
    if time.time() > timeout:
        break

print("switch2")
timeout = time.time() + sleep
previous_time = time.time()
drone.send(at.CONFIG("video:video_channel", 1))
while True:
    ret, img = cam.read
    current_time = time.time()-previous_time
    print("ret:", ret, '/time:', current_time)
    if ret:
        cv2.imshow(" img", img)
        cv2.waitKey(1)
    if time.time() > timeout:
        break

print("switch3")
drone.send(at.CONFIG("video:video_channel", 0))
previous_time = time.time()
timeout = time.time() + sleep

while True:
    ret, img = cam.read()
    current_time = time.time()-previous_time
    print("ret:", ret, '/time:', current_time)
    if ret:
        cv2.imshow(" img", img)
        cv2.waitKey(1)
    if time.time() > timeout:
        break
