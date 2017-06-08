import time
from pyardrone import ARDrone, at

print("Start Programme")


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


def nav_data(uav, previous_time, previous_vx, vx_distance, vy_distance):

    vx = uav.navdata.demo.vx
    vy = uav.navdata.demo.vy
    altitude = drone.navdata.demo.altitude

    if vx != previous_vx:
        time_difference = time.time() - previous_time

        new_vx_distance = time_difference * vx
        vx_distance = vx_distance + new_vx_distance

        new_vy_distance = time_difference * vy
        vy_distance = vy_distance + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t vy = ", new_vy_distance, "\t\t Total x = ", vx_distance,
              "\t\t Total y = ", vy_distance,  "\t\t Altitude = ", altitude)

        previous_time = time.time()
        previous_vx = vx

        return[previous_time, previous_vx, vx_distance, vy_distance, altitude]

Position = [0, 0, 0, 0, 0]

drone = init()

print("Take-off..")
while not drone.state.fly_mask:
    PreviousTime = time.time()
    Position = nav_data(drone, Position[0], Position[1], Position[2], Position[3])
    drone.takeoff()

print("Hovering")
timeout = time.time()+5
while True:
    drone.hover()
    Position = nav_data(drone, Position[0], Position[1], Position[2], Position[3])
    if time.time() > timeout:
        break

print("Going up")
while True:
    drone.hover()
    Position = nav_data(drone, Position[0], Position[1], Position[2], Position[3])

print("Landing")
while drone.state.fly_mask:
    drone.land()
    Position = nav_data(drone, Position[0], Position[1], Position[2], Position[3])

print("Finished")
