from pyardrone import ARDrone

drone = ARDrone()

print("Landing")
while drone.state.fly_mask:
    drone.land()
exit()

