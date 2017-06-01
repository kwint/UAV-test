import time
from pyardrone import ARDrone, at
drone = ARDrone()

speed = 0.1
sleep = 1

print("Connecting")
drone.navdata_ready.wait()  # wait until NavData is ready
print("Ready")
drone.takeoff()
print("TakeOff!")
time.sleep(1)

timeout = time.time() + 10
print("CW", speed)
while True:
    drone.move(cw=0.2)
    if time.time() > timeout:
        break

drone.move(cw=0)
print("stop")
time.sleep(1)

drone.land()
print("LANDING")

exit()


# drone.move(backward=speed)
# print("Backward", speed)
# time.sleep(sleep)
# drone.move(backward=0)
# print("stop")
# drone.move(left=speed)
# print("Left", speed)
# time.sleep(sleep)
# drone.move(left=0)
# print("stop")
# drone.move(right=speed)
# print("Right", speed)
# time.sleep(sleep)
# drone.move(right=0)
# print("stop")
# drone.move(cw=speed)
# print("CW", speed)
# drone.move(cw=0)
# print("stop")
# drone.move(ccw=speed)
# print("CCW", speed)
# time.sleep(sleep)
# drone.move(ccw=0)
# print("stop")
# drone.land()
# print("LANDING")