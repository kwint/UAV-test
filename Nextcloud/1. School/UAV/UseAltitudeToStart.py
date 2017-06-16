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

drone = init()

print("Take-off..")
while not drone.state.fly_mask:
    PreviousTime = time.time()
    drone.takeoff()

print("Hovering")
timeout = time.time()+5
altitude = drone.navdata.demo.altitude
while True:
    drone.hover()
    altitude_new = drone.navdata.demo.altitude
    if altitude_new != altitude:
        print(altitude)
        altitude = altitude_new
    if time.time() > timeout:
        break

print("Going up")

while altitude < 2000:
    drone.move(up=0.2)
    altitude_new = drone.navdata.demo.altitude
    if altitude_new != altitude:
        print(altitude)
        altitude = altitude_new
drone.move(up=0)

print("Forward")
timeout = time.time()+5
altitude = drone.navdata.demo.altitude
while True:
    drone.move(forward=0.1)
    altitude_new = drone.navdata.demo.altitude
    if altitude_new != altitude:
        print(altitude)
        altitude = altitude_new
    if time.time() > timeout:
        break

print("Backward")
timeout = time.time()+5
altitude = drone.navdata.demo.altitude
while True:
    drone.move(backward=0.1)
    altitude_new = drone.navdata.demo.altitude
    if altitude_new != altitude:
        print(altitude)
        altitude = altitude_new
    if time.time() > timeout:
        break


print("Landing")
while drone.state.fly_mask:
    drone.land()

print("Finished")
