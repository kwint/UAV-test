import time
from pyardrone import ARDrone
drone = ARDrone()
print("1")
drone.navdata_ready.wait()  # wait until NavData is ready
print("2")
while not drone.state.fly_mask:
    print("3")
    drone.takeoff()
    print("4")
time.sleep(20)              # hover for a while
print("5")
while drone.state.fly_mask:
    print("6")
    drone.land()
    print("7")