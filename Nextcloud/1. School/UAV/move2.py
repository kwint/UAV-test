from pyardrone import ARDrone, at
import cv2
import time

def takePicture(drone, marker, hight, cam):

    timeout = time.time() + 10
    while time.time() < timeout:
        drone.send(at.CONFIG("video:video_channel", 0))
        drone.hover()

    ret, img = cam.read()

    if ret:
        string = str(time.ctime()) + str(marker) + str(hight) + ".jpg"
        print(string)
        cv2.imwrite('C:\\' + string, img)
        cv2.imshow(string, img)
        print("saved image")
    time.sleep(0.1)

    drone.send(at.CONFIG("video:video_channel", 1))
    timeout = time.time() + 3
    while time.time() < timeout:
        drone.hover()
    return


def droneMove(moveData, drone, goBack):
    timeout = time.time() + 0.5
    while True:
        if moveData.marker:

            if moveData.dir_x == 1:
                drone.move(forward=moveData.speed_x)
            elif moveData.dir_y == 0:
                drone.move(backward=moveData.speed_x)

            if moveData.dir_y == 1:
                drone.move(right=moveData.speed_y)
            elif moveData.dir_y == 0:
                drone.move(left=moveData.speed_y)
            if time.time() > timeout:
                break

            timeout = time.time() + 1
            while True:
                drone.move(forward=0, left=0, right=0, backward=0)
                drone.hover()
                if time.time() > timeout:
                    break
        else:
            if not goBack:
                timeout = time.time() + 0.5
                while True:
                    drone.move(left=moveData.speed_y)
                    if time.time() > timeout:
                        break

                timeout = time.time() + 1
                while True:
                    drone.move(forward=0, left=0, right=0, backward=0)
                    drone.hover()
                    if time.time() > timeout:
                        break
            else:
                timeout = time.time() + 0.5
                while True:
                    drone.move(right=moveData.speed_y)
                    if time.time() > timeout:
                        break

                timeout = time.time() + 1
                while True:
                    drone.move(forward=0, left=0, right=0, backward=0)
                    drone.hover()
                    if time.time() > timeout:
                        break

    pass
