import time
from pyardrone import ARDrone, at

print("hallotjes")


def init():
    uav = ARDrone()
    print("ready to wait2")
    uav.navdata_ready.wait()
    print("ready")
    uav.send(at.CONFIG('general:navdata_demo', True))
    time.sleep(0.1)
    print("send")
    while uav.state.emergency_mask:
        print("emergency")
        uav.send(at.REF(0b0100000000))
        time.sleep(1)
    print("ready1")
    return uav

drone = init()

while not drone.state.fly_mask:
    drone.takeoff()
    print("Vlieg op!")
print("JA baas")

drone.hover()
print("hover")
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
        TimeDifference = time.time() - PreviousTime

        NewVxDistance = TimeDifference * vx
        VxDistance = VxDistance + NewVxDistance

        NewVyDistance = TimeDifference * vy
        VyDistance = VyDistance + NewVyDistance

        print("vx = ", NewVxDistance, "vy = ", NewVyDistance, "TotalX = ", VxDistance, "TotalY = ", VyDistance)

        PreviousTime = time.time()

print("klaar")
while drone.state.fly_mask:
    drone.land()
    print("ga landen maat")

print("doei")
