import time
import cv2

cam = cv2.VideoCapture(0)
ret, img = cam.read()

tijd = time.ctime()
print(tijd)
tijd = tijd.replace(" ", "_")
tijd = tijd.replace(":", "_")
cv2.imwrite(tijd + ".jpg", img)
print(tijd)