import time
from pyardrone import ARDrone, at

def getdata(drone):
    while True:
        # get data process here
        print(drone.navdata.demo)
        navdata = drone.navdata.demo
        print(navdata)
        print(type(navdata))
        time.sleep(2)
