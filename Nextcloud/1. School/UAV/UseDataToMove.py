import time
from pyardrone import ARDrone, at


def init():
    uav = ARDrone()
    uav.navdata_ready.wait()
    print("ready")
    uav.send(at.CONFIG('general:navdata_demo', True))
    time.sleep(0.1)
    print("send")
    while uav.state.emergency_mask:
        print("emergency")
        uav.send(at.REF(0b0100000000))
        time.sleep(1)
    print("ready")
    return uav


def get_data(drone):                                    #get money, get bitches, get DATA <3
    altitude = drone.navdata.demo.altitude
    vx = drone.navdata.demo.vx
    vy = drone.navdata.demo.vy
    vz = drone.navdata.demo.vz
    phi = drone.navdata.demo.phi
    psi = drone.navdata.demo.psi
    theta = drone.navdata.demo.theta
    return (altitude, vx, vy, vz, phi, psi, theta)


def data_print(drone, previous_data):
    current_data = get_data(drone)
    if (previous_data!=current_data):
        print("Altitude: ", previous_data[0], "\t vx: ", previous_data[1], "\t vy: ", previous_data[2], "\t vz: ", previous_data[3], "\t phi: ", previous_data[4], "\t psi: ", previous_data[5],
              "\t theta: ", previous_data[6])
    return(current_data)

drone = init()
print("connecting")
previous_data = get_data(drone)

previous_data = data_print(drone, previous_data)

speed = 0.1
ActionTime = 2
SleepTime = 1

while not drone.state.fly_mask:
    drone.takeoff()
    print("Vlieg op!")

print("JA baas")

drone.hover()
print("hover")
time.sleep(SleepTime*3)

print("Omhoog")
timeout = time.time() + ActionTime
while True:
    drone.move(up=speed*4)
    previous_data = data_print(drone, previous_data)
    if time.time() > timeout:
        drone.move(up=0)
        break

drone.hover()
print("hover")
time.sleep(SleepTime)

print("Vooruit met die geit")
timeout = time.time() + ActionTime
while True:
    drone.move(forward=speed)
    previous_data = data_print(drone, previous_data)
    if time.time() > timeout:
        drone.move(forward=0)
        break

drone.hover()
print("hover")
time.sleep(SleepTime)

print("Rechts")
timeout = time.time() + ActionTime
while True:
    drone.move(right=speed)
    previous_data = data_print(drone, previous_data)
    if time.time() > timeout:
        drone.move(right=0)
        break

drone.hover()
print("hover")
time.sleep(SleepTime)

print("en een stapje terug")
timeout = time.time() + ActionTime
while True:
    drone.move(backward=speed)
    previous_data = data_print(drone, previous_data)
    if time.time() > timeout:
        drone.move(backward=0)
        break

drone.hover()
print("hover")
time.sleep(SleepTime)

print("Links")
timeout = time.time() + ActionTime
while True:
    drone.move(left=speed)
    previous_data = data_print(drone, previous_data)
    if time.time() > timeout:
        drone.move(left=0)
        break

drone.hover()
print("hover")
time.sleep(SleepTime)

print("Omlaag")
timeout = time.time() + ActionTime
while True:
    drone.move(down=speed*4)
    previous_data = data_print(drone, previous_data)
    if time.time() > timeout:
        drone.move(down=0)
        break

print("klaar")

while drone.state.fly_mask:
    drone.land()
    # print("ga landen maat")

print("doei")

previous_data = data_print(drone, previous_data)
exit()
