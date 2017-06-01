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
        time.sleep(0.1)
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
        print("Altitude: ", altitude, "\t vx: ", vx, "\t vy: ", vy, "\t vz: ", vz, "\t phi: ", phi, "\t psi: ", psi,
              "\t theta: ", theta)

    return(current_data)

drone = init()
print("connecting")
previous_data = get_data(drone)

previous_data = data_print(drone, previous_data)

while not drone.state.fly_mask:
    drone.takeoff()
    print("Vlieg op!")

print("JA baas")

timeout = time.time() + 10
while True:
    drone.hover()
    previous_data = data_print(drone, previous_data)
    if time.time() > timeout:
        print("hij is van de andere kant")
        break

print("klaar")

while drone.state.fly_mask:
    drone.land()
    # print("ga landen maat")

print("doei")

previous_data = data_print(drone, previous_data)
exit()
