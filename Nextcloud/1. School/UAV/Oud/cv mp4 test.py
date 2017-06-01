import cv2
import sys
cap = cv2.VideoCapture(1)

ret, frame = cap.read()
if not ret:
    print("capture failed")