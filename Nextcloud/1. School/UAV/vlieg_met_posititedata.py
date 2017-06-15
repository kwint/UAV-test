import time
import numpy as np
from pyardrone import ARDrone, at

print("Start Program")


def init():
    uav = ARDrone()
    print("Initiating - waiting..")
    uav.navdata_ready.wait()
    print("NavData Ready")
    uav.send(at.CONFIG('general:navdata_demo', True))
    time.sleep(0.1)
    print("Battery = ", uav.navdata.demo.vbat_flying_percentage)

    while uav.state.emergency_mask:
        print("Emergency")
        uav.send(at.REF(0b0100000000))
        time.sleep(1)

    if uav.state.vbat_low:
        print("Battery to low")
    elif uav.state.video_mask == 0:
        print("Video Disabled")
    elif uav.state.vision_mask == 0:
        print("Vision Disabled")
    elif uav.state.altitude_mask == 0:
        print("Altitude control inactive")
    elif uav.state.camera_mask == 0:
        print("Camera not ready")
    elif uav.state.travelling_mask == 0:
        print("Travelling mask disabled")
    elif uav.state.usb_mask == 0:
        print("USB key not ready")
    elif uav.state.navdata_demo_mask == 0:
        print("navdata demo not activated")
    elif uav.state.navdata_bootstrap:
        print("no navdata options send")
    elif uav.state.motors_mask:
        print("Motors problem")
    elif uav.state.com_lost_mask:
        print("Communication problem")
    elif uav.state.software_fault:
        print("Software fault detected")
    elif uav.state.magneto_needs_calib:
        print("Magneto calibration needed")
    elif uav.state.angles_out_of_range:
        print("angles_out_of_range")
    elif uav.state.wind_mask:
        print("Too much wind")
    elif uav.state.ultrasound_mask:
        print("Ultrasonic sensor deaf")
    elif uav.state.cutout_mask:
        print("Cutout system detected")
    else:
        print("Ready")
    return uav


def nav_data(uav, previous_vx, previous_time, previous_distance_vx, previous_distance_vy):
    vx = uav.navdata.demo.vx
    if vx != previous_vx:

        vy = uav.navdata.demo.vy
        altitude = uav.navdata.demo.altitude

        time_difference = time.time() - previous_time

        new_vx_distance = time_difference * vx
        previous_distance_vx = previous_distance_vx + new_vx_distance

        new_vy_distance = time_difference * vy
        previous_distance_vy = previous_distance_vy + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t vy = ", new_vy_distance, "\t\t Total x = ", previous_distance_vx,
              "\t\t Total y = ", previous_distance_vy,  "\t\t Altitude = ", altitude)

        previous_vx = vx
        previous_time = time.time()

        return previous_vx, previous_time, previous_distance_vx, previous_distance_vy, altitude

Position = [0.1, 0.1, 0.1, 0.1, 0]

drone = init()

print("Take-off..")
while not drone.state.fly_mask:
    PreviousTime = time.time()
    Position = nav_data(drone, Position[0], Position[1], Position[2], Position[3])
    #drone.takeoff()

print("Hovering")
timeout = time.time()+5
while True:
    drone.hover()
    Position = nav_data(drone, Position)
    if time.time() > timeout:
        break

print("Going up")

while Position[4] < 700.0:
    drone.move(up=0.3)
    Position = nav_data(drone, Position)
drone.move(up=0)

print("Landing")
while drone.state.fly_mask:
    drone.land()
    Position = nav_data(drone, Position)

print("Finished")
