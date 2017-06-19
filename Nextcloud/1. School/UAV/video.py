import cv2
import time
import numpy as np
from pyardrone import ARDrone, at
import threading

import move


def nothing(x):
    pass


def init():
    uav = ARDrone()
    print("Initiating - waiting..")
    uav.navdata_ready.wait()
    print("NavData Ready")
    uav.send(at.CONFIG('general:navdata_demo', True))
    time.sleep(0.1)
    uav.send(at.CONFIG("video:video_channel", 1))
    time.sleep(0.1)
    print("Battery = ", uav.navdata.demo.vbat_flying_percentage)

    if uav.state.vbat_low:
        print("Battery to low, please replace before flying")
        exit()
    if uav.state.video_mask == 0:
        print("Video Disabled")
    if uav.state.vision_mask == 0:
        print("Vision Disabled")
    if uav.state.altitude_mask == 0:
        print("Altitude control inactive")
    if uav.state.camera_mask == 0:
        print("Camera not ready")
    if uav.state.travelling_mask == 0:
        print("Travelling mask disabled")
    if uav.state.usb_mask == 0:
        print("USB key not ready")
    if uav.state.navdata_demo_mask == 0:
        print("navdata demo not activated")
    if uav.state.navdata_bootstrap:
        print("no navdata options send")
    if uav.state.motors_mask:
        print("Motors problem")
    if uav.state.com_lost_mask:
        print("Communication problem")
    if uav.state.software_fault:
        print("Software fault detected")
    if uav.state.magneto_needs_calib:
        print("Magneto calibration needed")
    if uav.state.angles_out_of_range:
        print("angles_out_of_range")
    if uav.state.wind_mask:
        print("Too much wind")
    if uav.state.ultrasound_mask:
        print("Ultrasonic sensor deaf")
    if uav.state.cutout_mask:
        print("Cutout system detected")

    while uav.state.emergency_mask:
        print("Emergency")
        uav.send(at.REF(0b0100000000))
        time.sleep(0.1)

    # Create windows and sliders
    cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)

    cv2.namedWindow('slider', cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow('slider', 640, 0)
    cv2.resizeWindow('slider', 560, 400)
    cv2.createTrackbar('B', 'slider', 0, 255, nothing)
    cv2.createTrackbar('G', 'slider', 0, 255, nothing)
    cv2.createTrackbar('R', 'slider', 0, 255, nothing)

    cv2.createTrackbar('B1', 'slider', 0, 255, nothing)
    cv2.createTrackbar('G1', 'slider', 0, 255, nothing)
    cv2.createTrackbar('R1', 'slider', 0, 255, nothing)

    cv2.createTrackbar('kernel', 'slider', 1, 20, nothing)
    cv2.setTrackbarPos('kernel', 'slider', 2)

    return uav


def filter_image(img, lower_mask, upper_mask):
    # set sliders to start values

    cv2.setTrackbarPos('B', 'slider', lower_mask[0])
    cv2.setTrackbarPos('G', 'slider', lower_mask[1])
    cv2.setTrackbarPos('R', 'slider', lower_mask[2])
    cv2.setTrackbarPos('B1', 'slider', upper_mask[0])
    cv2.setTrackbarPos('G1', 'slider', upper_mask[1])
    cv2.setTrackbarPos('R1', 'slider', upper_mask[2])

    # wait a bit to update
    cv2.waitKey(5)

    # Read slider positions
    b = cv2.getTrackbarPos('B', 'slider')
    g = cv2.getTrackbarPos('G', 'slider')
    r = cv2.getTrackbarPos('R', 'slider')
    b1 = cv2.getTrackbarPos('B1', 'slider')
    g1 = cv2.getTrackbarPos('G1', 'slider')
    r1 = cv2.getTrackbarPos('R1', 'slider')
    kernelsize = cv2.getTrackbarPos('kernel', 'slider')
    kernel = np.ones((kernelsize, kernelsize), np.uint8)

    # Build mask array from sliders
    lower_unit = np.array([b, g, r])
    upper_unit = np.array([b1, g1, r1])

    # Convert image to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Filter colors
    mask = cv2.inRange(hsv, lower_unit, upper_unit)
    res = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow("res", res)

    # Convert to grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # Make binary image
    ret, thres = cv2.threshold(gray, 20, 255, 0)

    # Close some holes
    thres = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)

    # Return binary image and slider data, so program remebers their position
    return thres, b, g, r, b1, g1, r1


def takeoff(drone):
    print("Take-off..")
    while not drone.state.fly_mask:
        drone.takeoff()

    print("Hovering")
    timeout = time.time() + 6
    while True:
        drone.hover()
        if time.time() > timeout:
            break

    print("Going up")
    altitude = drone.navdata.demo.altitude
    while altitude < 1800:
        drone.move(up=0.2)
        altitude = drone.navdata.demo.altitude
    drone.move(up=0)

    print("Hovering")
    timeout = time.time() + 3
    while True:
        drone.hover()

        if time.time() > timeout:
            break


class MoveData:
    def __init__(self, marker, dir_x, speed_x, dir_y, speed_y):
        self.speed_y = speed_y
        self.dir_y = dir_y
        self.speed_x = speed_x
        self.dir_x = dir_x
        self.marker = marker


print("\tStarting Program")
cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
print("\tVideoCapture ready")
drone = init()

# Data for debuging
lower_mask = np.array([0, 4, 148])
upper_mask = np.array([255, 255, 255])
i = 1
ret = True

nextMarker = 1  # first marker
maxMarkers = 4  # number of markers +1
speed = 0.1  # speed of drone

lookForNextMarker = False
MarkerFound = False

# Create things for thread that moves the drone
moveData = MoveData(False, 0, speed, 0, speed)
movethread = threading.Thread(target=move.droneMove, args=(moveData, drone))

takeoff(drone)

while True:
    # img = cv2.imread("drone/img" + str(i) + ".jpg") # for testing with images

    ret, img = cam.read()  # Get picture from video feed
    if ret:  # If picture gotten

        # For setting color filtering settings, useful for different backgrounds
        thres, b, g, r, b1, g1, r1 = filter_image(img, lower_mask, upper_mask)
        lower_mask = [b, g, r]
        upper_mask = [b1, g1, r1]
        # cv2.imshow("thres", thres)
        try:
            im2, contours, hierarchy = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            hierarchy = hierarchy[0]
            print("hierarchy: ", hierarchy)

        except TypeError:
            # When contrours doesnt find anything
            print(" Ja Dat was me weer een errotje zeg")

        else:  # If contours found
            currentMarker = 0
            # area = np.array([[180, 0], [180, 360], [540, 360], [540, 0]])
            # cv2.drawContours(img, [area], 0, (255, 0, 0), 2)

            for component in zip(contours, hierarchy):
                currentContour = component[0]
                currentHierarchy = component[1]

                if 100 < cv2.contourArea(currentContour) < 50000:

                    print("currentHierarchy: ", currentHierarchy)
                    if currentHierarchy[2] >= 0 and currentHierarchy[3] >= 0:  # if contour has a child and a parent
                        # Draw box around contours
                        rect = cv2.minAreaRect(currentContour)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)

                        # currentContour should be black square, check if its parent doesnt have a parent and its child
                        # doesnt have a child
                        if hierarchy[currentHierarchy[2]][2] < 0 and hierarchy[currentHierarchy[3]][3] < 0:
                            # Probably found a marker, yeey!
                            MarkerContourOutside = contours[currentHierarchy[3]]
                            MarkerContourInside = currentContour
                            print("Contour area ratio: ",
                                  cv2.contourArea(MarkerContourInside) / cv2.contourArea(MarkerContourOutside))

                            # Draw box around contours
                            rect2 = cv2.minAreaRect(MarkerContourOutside)
                            box2 = cv2.boxPoints(rect2)
                            box2 = np.int0(box2)

                            # Found and printed marker contours above. Now check for circles in it.
                            circleContour = contours[currentHierarchy[2]]
                            circleHierarchy = hierarchy[currentHierarchy[2]]
                            currentMarker = 0
                            breakNext = False

                            if circleHierarchy[0] == -1:
                                breakNext = True

                            while True:
                                print(circleHierarchy)
                                rect3 = cv2.minAreaRect(circleContour)
                                box3 = cv2.boxPoints(rect3)
                                box3 = np.int0(box3)
                                cv2.drawContours(img, [box3], 0, (255, 0, 0), 2)
                                currentMarker += 1
                                circleHierarchy = hierarchy[circleHierarchy[0]]
                                circleContour = contours[circleHierarchy[0]]

                                if breakNext:
                                    break

                                if circleHierarchy[0] == -1:
                                    breakNext = True

                            # If the marker found is the marker we're looking for calculate its distance to the center
                            # of the image
                            if currentMarker == nextMarker:
                                lookForNextMarker = False
                                moveData.marker = True
                                moments = cv2.moments(MarkerContourOutside)

                                cx = int(moments['m10'] / moments['m00'])
                                cy = int(moments['m01'] / moments['m00'])

                                dx = cx - 320
                                dy = cy - 180
                                distanceToCenter = np.sqrt(dx * dx + dy * dy)
                                cv2.line(img, (cx, cy), (320, 180), (0, 255, 0), thickness=4)
                                print("D: ", distanceToCenter)
                                if distanceToCenter < 40:  # If close to center, we are above the marker!
                                    nextMarker = currentMarker + 1
                                    print("JAAAA IK BEN OP EEN MARKER, LETS MAKE A PICTURE MATES")
                                    move.takePicture(drone, currentMarker, 1, cam)
                                    lookForNextMarker = True
                                    if nextMarker == maxMarkers:
                                        nextMarker = 1
                                        print("Landing")
                                        while drone.state.fly_mask:
                                            drone.land()
                                        exit()

                                if dx > 0:
                                    # move right
                                    cv2.putText(img, "Move: Right", (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255))
                                    moveData.dir_y = 0

                                else:
                                    # move left
                                    cv2.putText(img, "Move: Left", (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255))
                                    moveData.dir_y = 1
                                if dy > 0:
                                    # move back
                                    cv2.putText(img, "Move: back", (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255))
                                    moveData.dir_x = 0
                                else:
                                    # move left
                                    cv2.putText(img, "Move: forward", (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255))
                                    moveData.dir_x = 1

                                # Print more!

                                cv2.putText(img, str(currentMarker), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255))
                                print("marker = ", currentMarker)

                                cv2.drawContours(img, [box2], 0, (0, 255, 255), 2)
                                cv2.drawContours(img, [box], 0, (255, 255, 255), 2)
                            else:
                                cv2.drawContours(img, [box2], 0, (0, 0, 0), 2)
                                cv2.drawContours(img, [box], 0, (0, 0, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if not movethread.is_alive() and moveData.marker:
            movethread = threading.Thread(target=move.droneMove, args=(moveData, drone))
            movethread.start()
            moveData.marker = False

        if not movethread.is_alive() and not moveData.marker:
            movethread = threading.Thread(target=move.droneMove, args=(moveData, drone))
            movethread.start()
        # time.sleep(3)
        i = 23
        # i += 1
        if i > 35:
            i = 0
