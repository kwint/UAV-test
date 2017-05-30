#!/usr/bin/env python

# Copyright (c) 2011 Bastian Venthur
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Demo app for the AR.Drone.

This simple application allows to control the drone and see the drone's video
stream.
"""


import pygame

from pyardrone import ARDrone, at

speed = 0.1

pygame.init()
W, H = 320, 240
screen = pygame.display.set_mode((W, H))
drone = ARDrone()
drone.send(at.CONFIG('general:navdata_demo', True))
drone.send(at.REF(0b0100000000))
drone.navdata_ready.wait()  # wait until NavData is ready
print("Ready")
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
        surface = pygame.image.fromstring(drone.image, (W, H), 'RGB')
        # battery status
        hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
        bat = drone.navdata.get(0, dict()).get('battery', 0)
        f = pygame.font.Font(None, 20)
        hud = f.render('Battery: %i%%' % bat, True, hud_color)
        screen.blit(surface, (0, 0))
        screen.blit(hud, (10, 10))
    except:
        pass

    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

print("Shutting down...")
drone.close()
print("Ok.")


