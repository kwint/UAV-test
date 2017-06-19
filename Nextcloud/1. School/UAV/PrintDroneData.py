import time
import cv2
import pyardrone
from pyardrone import ARDrone, at

drone = ARDrone()
print("Initiating - waiting..")
drone.navdata_ready.wait()
print("NavData Ready")

while True:
    x = str(pyardrone.navdata.options.VisionDetect.camera_source)
    print(x)




