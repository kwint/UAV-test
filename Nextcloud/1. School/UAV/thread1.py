import thread2

import threading
import time
import thread2
from pyardrone import ARDrone, at
import pygame
import cv2

class GetNavData(threading.Thread):
    def __init__(self, threadID, drone):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.drone = drone

    def run(self):
        print("Starting ")
        thread2.getdata(drone)
        print("Exiting ")


def init():
    drone = ARDrone()
    drone.send(at.CONFIG('general:navdata_demo', True))
    drone.send(at.REF(0b0100000000))
    print("send")
    return drone

cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
# Connect to drone and send some commands to it
drone = init()

drone.navdata_ready.wait()  # wait until NavData is ready
print("ready")
# Create new threads
thread1 = GetNavData(1, drone)

# Start new Threads
thread1.start()
pygame.init()
W, H = 320, 240
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            drone.hover()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                drone.send(at.REF(0b0100000000))
                running = False
            # takeoff / land
            elif event.key == pygame.K_RETURN:
                drone.takeoff()
            elif event.key == pygame.K_SPACE:
                drone.land()
            # emergency
            elif event.key == pygame.K_BACKSPACE:
                drone.send(at.REF(0b0100000000))
            # forward / backward
            elif event.key == pygame.K_w:
                drone.move(forward=speed)
            elif event.key == pygame.K_s:
                drone.move(backward=speed)
            # left / right
            elif event.key == pygame.K_a:
                drone.move(left=speed)
            elif event.key == pygame.K_d:
                drone.move(right=speed)
            # up / down
            elif event.key == pygame.K_UP:
                drone.move(up=speed)
            elif event.key == pygame.K_DOWN:
                drone.move(down=speed)
            # turn left / turn right
            elif event.key == pygame.K_LEFT:
                drone.move(ccw=speed)
            elif event.key == pygame.K_RIGHT:
                drone.move(cw=speed)
            # speed
            elif event.key == pygame.K_1:
                speed = 0.1
            elif event.key == pygame.K_2:
                speed = 0.2
            elif event.key == pygame.K_3:
                speed = 0.3
            elif event.key == pygame.K_4:
                speed = 0.4
            elif event.key == pygame.K_5:
                speed = 0.5
            elif event.key == pygame.K_6:
                speed = 0.6
            elif event.key == pygame.K_7:
                speed = 0.7
            elif event.key == pygame.K_8:
                speed = 0.8
            elif event.key == pygame.K_9:
                speed = 0.9
            elif event.key == pygame.K_0:
                speed = 1.0

    try:
        print("try build in ding")
        surface = pygame.image.fromstring(drone.frame, (W, H), 'RGB')
        # battery status
        hud_color = (255, 0, 0)
        bat = 100
        f = pygame.font.Font(None, 20)
        hud = f.render('Battery: %i%%' % bat, True, hud_color)
        screen.blit(surface, (0, 0))
        screen.blit(hud, (10, 10))
        print("gelukt")
    except:
        pass
    try:
        print("opencv test")
        _, img = cam.read()
        cv2.imshow("test", img)
        cv2.waitKey(1)
    except:
        pass

    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

print("Shutting down...")
drone.close()
print("Ok.")