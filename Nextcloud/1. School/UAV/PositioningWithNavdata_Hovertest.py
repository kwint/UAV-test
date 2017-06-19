import time
import numpy as np
from pyardrone import ARDrone, at


def init():
    uav = ARDrone()
    print("Initiating - waiting..")
    uav.navdata_ready.wait()
    print("NavData Ready")
    uav.send(at.CONFIG('general:navdata_demo', True))
    time.sleep(0.1)
    uav.send(at.CONFIG("video:video_channel", 1))
    time.sleep(0.1)
    print("Battery = ", uav.navdata.demo.vbat_flying_percentage)

    if uav.state.vbat_low:
        print("Battery to low, please replace before flying")
        exit()
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
        print("Self-test: All Clear")

    while uav.state.emergency_mask:
        print("Emergency")
        uav.send(at.REF(0b0100000000))
        time.sleep(1)

    return uav

drone = init()
previous_vx = 0
previous_distance_vx = 0
previous_distance_vy = 0

print("Take-off..")
while not drone.state.fly_mask:
    drone.takeoff()

print("Hovering")
previous_time = time.time()
timeout = time.time()+5
while True:
    drone.hover()

    vx = drone.navdata.demo.vx
    if vx != previous_vx:
        vy = drone.navdata.demo.vy
        altitude = drone.navdata.demo.altitude

        time_difference = time.time() - previous_time

        new_vx_distance = time_difference * vx
        previous_distance_vx = previous_distance_vx + new_vx_distance

        new_vy_distance = time_difference * vy
        previous_distance_vy = previous_distance_vy + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t\t vy = ", new_vy_distance, "\t\t\t Total x = ", previous_distance_vx,
              "\t\t\t Total y = ", previous_distance_vy, "\t\t\t Altitude = ", altitude)

        previous_vx = vx
        previous_time = time.time()

    if time.time() > timeout:
        break

print("Going up")
previous_time = time.time()
while altitude < 1800:
    drone.move(up=0.5)
    vx = drone.navdata.demo.vx
    if vx != previous_vx:
        vy = drone.navdata.demo.vy
        altitude = drone.navdata.demo.altitude

        time_difference = time.time() - previous_time

        new_vx_distance = time_difference * vx
        previous_distance_vx = previous_distance_vx + new_vx_distance

        new_vy_distance = time_difference * vy
        previous_distance_vy = previous_distance_vy + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t vy = ", new_vy_distance, "\t\t Total x = ", previous_distance_vx,
              "\t\t Total y = ", previous_distance_vy, "\t\t Altitude = ", altitude)

        previous_vx = vx
        previous_time = time.time()
drone.move(up=0)

print("Hovering")
previous_time = time.time()
timeout = time.time()+3
while True:
    drone.hover()

    vx = drone.navdata.demo.vx
    if vx != previous_vx:
        vy = drone.navdata.demo.vy
        altitude = drone.navdata.demo.altitude

        time_difference = time.time() - previous_time

        new_vx_distance = time_difference * vx
        previous_distance_vx = previous_distance_vx + new_vx_distance

        new_vy_distance = time_difference * vy
        previous_distance_vy = previous_distance_vy + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t\t vy = ", new_vy_distance, "\t\t\t Total x = ", previous_distance_vx,
              "\t\t\t Total y = ", previous_distance_vy, "\t\t\t Altitude = ", altitude)

        previous_vx = vx
        previous_time = time.time()

    if time.time() > timeout:
        break

print("Right")
timeout = time.time()+3
while True:
    drone.move(right=0.1)
    vx = drone.navdata.demo.vx
    if vx != previous_vx:
        vy = drone.navdata.demo.vy
        altitude = drone.navdata.demo.altitude

        time_difference = time.time() - previous_time

        new_vx_distance = time_difference * vx
        previous_distance_vx = previous_distance_vx + new_vx_distance

        new_vy_distance = time_difference * vy
        previous_distance_vy = previous_distance_vy + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t vy = ", new_vy_distance, "\t\t Total x = ", previous_distance_vx,
              "\t\t Total y = ", previous_distance_vy, "\t\t Altitude = ", altitude)

        previous_vx = vx
        previous_time = time.time()
    if time.time() > timeout:
        break

print("Hovering")
previous_time = time.time()
timeout = time.time()+3
while True:
    drone.hover()

    vx = drone.navdata.demo.vx
    if vx != previous_vx:
        vy = drone.navdata.demo.vy
        altitude = drone.navdata.demo.altitude

        time_difference = time.time() - previous_time

        new_vx_distance = time_difference * vx
        previous_distance_vx = previous_distance_vx + new_vx_distance

        new_vy_distance = time_difference * vy
        previous_distance_vy = previous_distance_vy + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t\t vy = ", new_vy_distance, "\t\t\t Total x = ", previous_distance_vx,
              "\t\t\t Total y = ", previous_distance_vy, "\t\t\t Altitude = ", altitude)

        previous_vx = vx
        previous_time = time.time()

    if time.time() > timeout:
        break

print("Left")
timeout = time.time()+3
while True:
    drone.move(left=0.1)
    vx = drone.navdata.demo.vx
    if vx != previous_vx:
        vy = drone.navdata.demo.vy
        altitude = drone.navdata.demo.altitude

        time_difference = time.time() - previous_time

        new_vx_distance = time_difference * vx
        previous_distance_vx = previous_distance_vx + new_vx_distance

        new_vy_distance = time_difference * vy
        previous_distance_vy = previous_distance_vy + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t vy = ", new_vy_distance, "\t\t Total x = ", previous_distance_vx,
              "\t\t Total y = ", previous_distance_vy, "\t\t Altitude = ", altitude)

        previous_vx = vx
        previous_time = time.time()
    if time.time() > timeout:
        break

print("Hovering")
previous_time = time.time()
timeout = time.time()+2
while True:
    drone.hover()

    vx = drone.navdata.demo.vx
    if vx != previous_vx:
        vy = drone.navdata.demo.vy
        altitude = drone.navdata.demo.altitude

        time_difference = time.time() - previous_time

        new_vx_distance = time_difference * vx
        previous_distance_vx = previous_distance_vx + new_vx_distance

        new_vy_distance = time_difference * vy
        previous_distance_vy = previous_distance_vy + new_vy_distance

        print("vx = ", new_vx_distance, "\t\t\t vy = ", new_vy_distance, "\t\t\t Total x = ", previous_distance_vx,
              "\t\t\t Total y = ", previous_distance_vy, "\t\t\t Altitude = ", altitude)

        previous_vx = vx
        previous_time = time.time()

    if time.time() > timeout:
        break

print("Landing")
while drone.state.fly_mask:
    drone.land()

print("Finished")
exit()
