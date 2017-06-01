import time
from pyardrone import ARDrone

drone = ARDrone()
drone.navdata_ready.wait()
print("ThreadDistance = Ready for Action")

VxDistance = 0
VyDistance = 0
PreviousTime = 0
PreviousVx = 0
PreviousVy = 0

while True:
    altitude = drone.navdata.demo.altitude
    vx = drone.navdata.demo.vx
    vy = drone.navdata.demo.vy
    vz = drone.navdata.demo.vz
    phi = drone.navdata.demo.phi
    psi = drone.navdata.demo.psi
    theta = drone.navdata.demo.theta

    if vx != PreviousVx:
        TimeDifference = time.time()-PreviousTime

        NewVxDistance = TimeDifference*vx
        VxDistance = VxDistance + NewVxDistance

        NewVyDistance = TimeDifference*vy
        VyDistance = VyDistance + NewVyDistance

        print("vx = ", NewVxDistance, "vy = ", NewVyDistance, "TotalX = ", VxDistance, "TotalY = ", VyDistance)

        PreviousTime = time.time()