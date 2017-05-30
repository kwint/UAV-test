import cv2
import time
import subprocess
from pyardrone import ARDrone, at, ARDroneBase, HelperMixin
# ffmpeg -i tcp://192.168.1.1:5555 -f image2 -update 1 img.bmp -y

cv2.namedWindow("test", cv2.WINDOW_AUTOSIZE)
drone = ARDrone()
drone.send(at.CONFIG("general:navdata_demo", True))
drone.send(at.CONFIG('video:video_channel', 2))

drone.navdata_ready.wait()
while not drone.state.fly_mask:
    print("vlieg!")
    drone.takeoff()
print("hover")
drone.hover()
time.sleep(5)
while drone.state.fly_mask:
    print("land")
    drone.land()
print("klaar")
drone.video_ready.wait()
print("ready")
print(drone.navdata.demo)

while True:
    try:
        img = cv2.imread("img.bmp")
        cv2.imshow("test", img)
        cv2.waitKey(2)
    except Exception:
        pass
# cam = cv2.VideoCapture("tcp://192.168.1.1:5555")

# try:
#     while True:
#         ret, img = cam.read()
#         cv2.imshow("hoi", img)
# except Exception:
#     print("foutje")
#
# try:
#     while True:
#
#         cv2.imshow("test", drone.frame)
# except Exception:
#     print("foutje")

print("stop?!")