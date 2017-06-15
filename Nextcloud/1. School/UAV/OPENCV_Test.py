
import time
import numpy as np
import cv2
cap = cv2.VideoCapture('tcp://192.168.1.1:5555')
#window = namedWindow("TheWindow",1)

import time
from pyardrone import ARDrone, at
def init():
    uav = ARDrone()
    uav.navdata_ready.wait()
    print("ready")
    time.sleep(0.1)
    print("send")
    while uav.state.emergency_mask:
        print("emergency")
        uav.send(at.REF(0b0100000000))
        time.sleep(1)
    print("ready")
    return uav


print ("Streaming...")

for i in range(1,2000):
   # Capture frame-by-frame
   ret, frame = cap.read()

   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   #cv2.imwrite('01.png', gray)

   #Using AKAZE descriptors.
   #detector = cv2.AKAZE_create()
   #(kps, descs) = detector.detectAndCompute(gray, None)
   #print("keypoints: {}, descriptors: {}".format(len(kps), descs.shape))

   # draw the keypoints and show the output image
   #cv2.drawKeypoints(frame, kps, frame, (0, 255, 0))

   cv2.imshow("DroneView", frame)

   k = cv2.waitKey(1)
   if k & 0xFF == ord('q'):
      break
   if (k == ord('a')):
      print("Move left")

print("klaar")

while drone.state.fly_mask:
    drone.land()
    # print("ga landen maat")

print("doei")

print ('Ending...')

#When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

