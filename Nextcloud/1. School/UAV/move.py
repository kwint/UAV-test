from pyardrone import ARdrone, at
import cv2
import time

def takePicture(drone, marker, hight):
    while cameraisnaarbeneden:
        drone.send(at.CONFIG("video:video_channel", 0))

    time.sleep(2)
    cv2.imwrite("result/"+ str(time.ctime()) + str(marker) + str(hight))
    print("saved image")

    while cameraisnaarvoren
        drone.send(at.CONFIG("video:video_channel", 1))
    time.sleep(2)
    return