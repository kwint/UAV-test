# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
# import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from pyardrone import ARDrone, at

drone = ARDrone()
drone.send(at.CONFIG('general:navdata_demo', True))
drone.send(at.REF(0b0100000000))
drone.emergency()
print("send")
drone.navdata_ready.wait()
drone.takeoff()

win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: Scrolling Plots')


# 3) Plot in chunks, adding one new plot curve for every 100 samples
chunkSize = 100
# Remove chunks after we have 10
maxChunks = 10
startTime = pg.ptime.time()
win.nextRow()
p5 = win.addPlot(colspan=2)
p5.setLabel('bottom', 'Time', 's')
p5.setXRange(-5, 0)
p5.showGrid(x=True, y=True)
curves = []
data = np.empty((chunkSize + 1, 2))
ptr = 0


def update_plot():
    global p5, data, ptr, curves
    now = pg.ptime.time()
    for c in curves:
        c.setPos(-(now - startTime), 0)

    i = ptr % chunkSize
    if i == 0:
        curve = p5.plot(pen=(0,255,0))
        curves.append(curve)
        last = data[-1]
        data = np.empty((chunkSize + 1, 2))
        data[0] = last
        while len(curves) > maxChunks:
            c = curves.pop(0)
            p5.removeItem(c)
    else:
        curve = curves[-1]
    data[i + 1, 0] = now - startTime
    data[i + 1, 1] = drone.navdata.demo.vx
    curve.setData(x=data[:i + 2, 0], y=data[:i + 2, 1])
    ptr += 1

curves2 = []
data2 = np.empty((chunkSize + 1, 2))
ptr2 = 0


def update_plot2():
    global p5, data2, ptr2, curves2
    now = pg.ptime.time()
    for c in curves2:
        c.setPos(-(now - startTime), 0)

    i = ptr2 % chunkSize
    if i == 0:
        curve2 = p5.plot(pen=(255,0,0))
        curves2.append(curve2)
        last = data2[-1]
        data2 = np.empty((chunkSize + 1, 2))
        data2[0] = last
        while len(curves2) > maxChunks:
            c = curves2.pop(0)
            p5.removeItem(c)
    else:
        curve2 = curves2[-1]
    data2[i + 1, 0] = now - startTime
    data2[i + 1, 1] = drone.navdata.demo.vy
    curve2.setData(x=data2[:i + 2, 0], y=data2[:i + 2, 1])
    ptr2 += 1



def get_navdata():
    return 2,4,8

def update():
    update_plot()
    update_plot2()

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

    ## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
