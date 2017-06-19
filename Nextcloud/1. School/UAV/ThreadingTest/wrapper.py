import threading

import time
from random import randint
import threading

queue = []


def produce(gegeven):
    for i in range(0, 10):
        print(gegeven.dirx)
        time.sleep(0.2)


class MoveData:
    def __init__(self, marker, dirx, speedx, diry, speedy):
        self.speedy = speedy
        self.diry = diry
        self.speedx = speedx
        self.dirx = dirx
        self.marker = marker


start = MoveData(True, 1, 1, 1, 1)

p = threading.Thread(target=produce, args=(start,))
p.start()
while True:
    print("hoi")
    if p.is_alive():
        print("hallo")
    else:
        print("dead")
        start.dirx = start.dirx + 1
        p = threading.Thread(target=produce, args=(start,))
        p.start()
        # help

    time.sleep(0.5)
