import time
import cv2
import pyardrone
from pyardrone import ARDrone, at

drone = ARDrone()
print("Initiating - waiting..")
drone.navdata_ready.wait()
print("NavData Ready")
drone.send(at.CONFIG('general:navdata_demo', True))
time.sleep(0.1)
drone.send(at.CONFIG("video:video_channel", 1))
time.sleep(0.1)
print("Battery = ", drone.navdata.demo.vbat_flying_percentage)

PreviousPhi = 0
PreviousTime = time.time()

while True:
    altitude = drone.navdata.demo.altitude
    vx = drone.navdata.demo.vx
    vy = drone.navdata.demo.vy
    vz = drone.navdata.demo.vz
    phi = drone.navdata.demo.phi
    psi = drone.navdata.demo.psi
    theta = drone.navdata.demo.theta

    if phi != PreviousPhi:
        TimeDifference = time.time()-PreviousTime

        print('\t\tpsi = ', psi,)

        PreviousTime = time.time()
        PreviousPhi = phi
