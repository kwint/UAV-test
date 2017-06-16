from pyardrone import at
import cv2
import time

def takePicture(drone, marker, hight):

    drone.send(at.CONFIG("video:video_channel", 0))

    time.sleep(3)
    cv2.imwrite("result/"+ str(time.ctime()) + str(marker) + str(hight))
    print("saved image")
    time.sleep(0.1)

    drone.send(at.CONFIG("video:video_channel", 1))
    time.sleep(2)
    return