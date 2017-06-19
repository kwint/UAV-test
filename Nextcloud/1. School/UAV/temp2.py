import numpy as np
import cv2
import time

imgs = ["Target1_1", "Target1_2", "Target2+3_1", "Target2+3_2", "Target 3_1", "Target3_2"]
prevmax = 0
for i in range(0, len(imgs)):
    tijd = time.time()
    print(imgs[i])
    img = cv2.imread(imgs[i] + ".jpg")
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    print(hist[0])
    print(hist[255])
    if hist[255] > prevmax:
        prevmax = hist[255]
    print(time.time() -tijd)

print(prevmax)