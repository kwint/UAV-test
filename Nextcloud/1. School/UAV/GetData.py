
# def getdata(drone):
#     while True:
#         # get data process here
#         print(drone.navdata.demo)

# -*- coding: utf-8 -*-
# """
# Various methods of drawing scrolling plots.
# """
# import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
# from pyardrone import ARDrone, at
# import threading
# import vlieg

global  curves_vx, data_vx, ptr_vx, \
        curves_vy, data_vy, ptr_vy
global drone, maxChunks, startTime, chunkSize, plot

print("getdata hoi")

def init():
    uav = ARDrone()
    print("ready to wait")
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

# drone = init()

win = pg.GraphicsWindow()
win.setWindowTitle('Plots waren daar plots')


# 3) Plot in chunks, adding one new plot curve for every 100 samples
chunkSize = 100
# Remove chunks after we have 10
maxChunks = 10
startTime = pg.ptime.time()
win.nextRow()
plot = win.addPlot(colspan=2)
plot.setLabel('bottom', 'Time', 's')
plot.setXRange(-5, 0)
plot.showGrid(x=True, y=True)

curves_vx = []
data_vx = np.empty((chunkSize + 1, 2))
ptr_vx = 0

curves_vy = []
data_vy = np.empty((chunkSize + 1, 2))
ptr_vy = 0

curves_vz = []
data_vz = np.empty((chunkSize + 1, 2))
ptr_vz = 0

print("init done")


def update_plot_vx():
    # print("update vx")
    global plot, data_vx, ptr_vx, curves_vx, startTime, chunkSize, maxChunks
    now = pg.ptime.time()
    for c in curves_vx:
        c.setPos(-(now - startTime), 0)

    i = ptr_vx % chunkSize
    if i == 0:
        curve = plot.plot(pen=(0, 255, 0))
        curves_vx.append(curve)
        last = data_vx[-1]
        data_vx = np.empty((chunkSize + 1, 2))
        data_vx[0] = last
        while len(curves_vx) > maxChunks:
            c = curves_vx.pop(0)
            plot.removeItem(c)
    else:
        curve = curves_vx[-1]
    data_vx[i + 1, 0] = now - startTime
    data_vx[i + 1, 1] = drone.navdata.demo.vx
    curve.setData(x=data_vx[:i + 2, 0], y=data_vx[:i + 2, 1])
    ptr_vx += 1




def update_plot_vy():
    # print("update vy")
    global plot, data_vy, ptr_vy, curves_vy, startTime, chunkSize, maxChunks
    now = pg.ptime.time()
    for c in curves_vy:
        c.setPos(-(now - startTime), 0)

    i = ptr_vy % chunkSize
    if i == 0:
        curve2 = plot.plot(pen=(255, 0, 0))
        curves_vy.append(curve2)
        last = data_vy[-1]
        data_vy = np.empty((chunkSize + 1, 2))
        data_vy[0] = last
        while len(curves_vy) > maxChunks:
            c = curves_vy.pop(0)
            plot.removeItem(c)
    else:
        curve2 = curves_vy[-1]
    data_vy[i + 1, 0] = now - startTime
    data_vy[i + 1, 1] = drone.navdata.demo.vy
    curve2.setData(x=data_vy[:i + 2, 0], y=data_vy[:i + 2, 1])
    ptr_vy += 1


def update():
    # print("update")
    update_plot_vx()
    update_plot_vy()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

# class threadtwee(threading.Thread):
#     def __init__(self, threadID, drone):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.drone = drone
#
#     def run(self):
#         print("Starting ")
#         vlieg.process(drone)
#         print("Exiting ")

# thread = threadtwee(1, drone)
# thread.start()

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()