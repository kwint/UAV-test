import time
from pyardrone import ARDrone, at

drone = ARDrone()
drone.navdata_ready.wait()
direction = drone.navdata.demo.psi

while drone.state.emergency_mask:
    print("Emergency")
    drone.send(at.REF(0b0100000000))
    time.sleep(1)

print(direction)

print("Take-off..")
while not drone.state.fly_mask:
    drone.takeoff()

time.sleep(20)

print("Check")

direction_difference = drone.navdata.demo.psi - direction
print(direction_difference)

if direction_difference < -10000:
    print("Turning CW")
    while drone.navdata.demo.psi < direction:
        drone.move(cw=0.1)


if direction_difference > 10000:
    print("Turning CCW")
    while drone.navdata.demo.psi > direction:
        drone.move(ccw=0.1)

print('position OK')

print("Landing")
while drone.state.fly_mask:
    drone.land()
exit()

