import cv2

cam = cv2.VideoCapture("tcp://192.168.1.1:5555")

while True:
    ret, img = cam.read()
    if ret:
        cv2.imshow("img", img)
        if cv2.waitKey(1) == 27:
            break

