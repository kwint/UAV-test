import cv2
import numpy as np
import time


def nothing(x):
    pass

cv2.xfeatures2d.SIFT_create()

def init():
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


init()
lower_mask = np.array([0, 4, 148])
upper_mask = np.array([255, 255, 255])
i = 1
cam = cv2.VideoCapture(0)
ret = True
while True:
    img = cv2.imread("drone/img" + str(i) + ".jpg")
    if ret:

        thres, b, g, r, b1, g1, r1 = filter_image(img, lower_mask, upper_mask)
        lower_mask = [b, g, r]
        upper_mask = [b1, g1, r1]
        # cv2.imshow("thres", thres)

        im2, contours, hierarchy = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        hierarchy = hierarchy[0]
        print("hierarchy: ", hierarchy)

        marker = 0
        MarkerInArea = True
        area = np.array([[180, 0], [180, 360], [540, 360], [540, 0]])
        cv2.drawContours(img, [area], 0, (255, 0, 0), 2)

        for component in zip(contours, hierarchy):
            currentContour = component[0]
            currentHierarchy = component[1]

            if 100 < cv2.contourArea(currentContour) < 50000:

                print("currentHierarchy: ", currentHierarchy)
                if currentHierarchy[2] >= 0 and currentHierarchy[3] >= 0:  # if contour has a child and a parent
                    # currentContour should be black square, check if its parent doenst have a parent and its child
                    # doesnt have a child
                    rect = cv2.minAreaRect(currentContour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    if hierarchy[currentHierarchy[2]][2] < 0 and hierarchy[currentHierarchy[3]][3] < 0:
                        # Probably found a marker, yeey!
                        MarkerContourOutside = contours[currentHierarchy[3]]
                        MarkerContourInside = currentContour
                        print("Contour ding: ", cv2.contourArea(MarkerContourInside)/cv2.contourArea(MarkerContourOutside))
                        rect2 = cv2.minAreaRect(MarkerContourOutside)
                        box2 = cv2.boxPoints(rect2)
                        box2 = np.int0(box2)
                        cv2.drawContours(img, [box2], 0, (0, 255, 255), 2)
                        cv2.drawContours(img, [box], 0, (255, 255, 255), 2)

                        # Found and printed marker contours above. No check for circles in it.
                        circleContour = contours[currentHierarchy[2]]
                        circleHierarchy = hierarchy[currentHierarchy[2]]
                        marker = 0
                        breakNext = False

                        if circleHierarchy[0] == -1:
                            breakNext = True
                            print("breakNext True")

                        print("Hier ben ik")
                        while True:
                            print(circleHierarchy)
                            rect3 = cv2.minAreaRect(circleContour)
                            box3 = cv2.boxPoints(rect3)
                            box3 = np.int0(box3)
                            cv2.drawContours(img, [box3], 0, (255, 0, 0), 2)
                            marker += 1
                            circleHierarchy = hierarchy[circleHierarchy[0]]
                            circleContour = contours[circleHierarchy[0]]

                            if breakNext:
                                print("gebroken")
                                break

                            if circleHierarchy[0] == -1:
                                breakNext = True
                                print("breakNext True")


                        moments = cv2.moments(MarkerContourOutside)

                        cx = int(moments['m10'] / moments['m00'])
                        cy = int(moments['m01'] / moments['m00'])

                        dx = cx - 320
                        dy = cy - 180
                        distanceToCenter = np.sqrt(dx * dx + dy * dy)
                        cv2.line(img, (cx, cy), (320, 180), (255, 255, 255))

                        if distanceToCenter > 0:
                            # move right
                            cv2.putText(img, "Move: Right", (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255))
                        if distanceToCenter < 0:
                            # move left
                            cv2.putText(img, "Move: Left", (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255))

        cv2.putText(img, str(marker), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255))
        print("marker = ", marker)

        # for component in zip(contours, hierarchy):
        #     currentContour = component[0]
        #     currentHierarchy = component[1]
        #     x, y, w, h = cv2.boundingRect(currentContour)
        #     print(currentHierarchy[2])
        #     if currentHierarchy[2] < 0:
        #         # these are the innermost child components
        #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #     elif currentHierarchy[3] < 0:
        #         # these are the outermost parent components
        #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        # time.sleep(3)
        i = 32
        # i += 1
        if i > 35:
            i = 0
            # print(hierarchy)
