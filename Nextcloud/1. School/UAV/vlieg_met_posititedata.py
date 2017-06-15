import time
from pyardrone import ARDrone, at

print("Start Program")


def init():
    uav = ARDrone()
    print("Initiating")
    uav.navdata_ready.wait()
    print("NavData Ready")
    uav.send(at.CONFIG('general:navdata_demo', True))
    time.sleep(0.1)
    while uav.state.emergency_mask:
        print("Emergency")
        uav.send(at.REF(0b0100000000))
        time.sleep(1)
    print("Ready")
    return uav


def nav_data(uav, previous):

    vx = uav.navdata.demo.vx

    if vx != previous[0]:

        vy = uav.navdata.demo.vy
        previous[4] = drone.navdata.demo.altitude

        time_difference = time.time() - previous[1]

        new_vx_distance = time_difference * vx
        previous[2] = previous[2] + new_vx_distance

        new_vy_distance = time_difference * vy
        previous[3] = previous[3] + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t vy = ", new_vy_distance, "\t\t Total x = ", previous[2],
              "\t\t Total y = ", previous[3],  "\t\t Altitude = ", previous[4])

        previous[0] = vx
        previous[1] = time.time()

        return[previous]

Position = [0, 0, 0, 0, 0]

drone = init()

print("Take-off..")
while not drone.state.fly_mask:
    PreviousTime = time.time()
    Position = nav_data(drone, Position)
    drone.takeoff()

print("Hovering")
timeout = time.time()+5
while True:
    drone.hover()
    Position = nav_data(drone, Position)
    if time.time() > timeout:
        break

print("Going up")
while (Position[4]<700):
    drone.move(up=0.3)
    Position = nav_data(drone, Position)
drone.move(up=0)

print("Landing")
while drone.state.fly_mask:
    drone.land()
    Position = nav_data(drone, Position)

print("Finished")
