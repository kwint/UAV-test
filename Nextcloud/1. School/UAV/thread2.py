# import time
# from pyardrone import ARDrone, at
#
# def getdata(drone):
#     while True:
#         # get data process here
#         print(drone.navdata.demo)
#         navdata = drone.navdata.demo
#         print(navdata)
#         print(type(navdata))
#         time.sleep(2)

# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
# import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
def getdata(dr):
        global drone, maxChunks, startTime, curves_vx, data_vx, ptr_vx, \
                                            curves_vy, data_vy, ptr_vy, \
                                            curves_vz, data_vz, ptr_vz
        drone = dr
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

        curves_vx = []
        data_vx = np.empty((chunkSize + 1, 2))
        ptr_vx = 0

        curves_vy = []
        data_vy = np.empty((chunkSize + 1, 2))
        ptr_vy = 0

        curves_vz = []
        data_vz = np.empty((chunkSize + 1, 2))
        ptr_vz = 0

        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(50)

        ## Start Qt event loop unless running in interactive mode or using pyside.
        if __name__ == '__main__':
            import sys

            if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                QtGui.QApplication.instance().exec_()


def update_plot_vx():
    global plot, data_vx, ptr_vx, curves_vx, startTime, chunkSize, maxChunks, drone
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
    global plot, data_vy, ptr_vy, curves_vy, startTime, chunkSize, maxChunks, drone
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


def update_plot_vz():
    global plot, data_vz, ptr_vz, curves_vz, startTime, chunkSize, maxChunks, drone
    now = pg.ptime.time()
    for c in curves_vz:
        c.setPos(-(now - startTime), 0)

    i = ptr_vz % chunkSize
    if i == 0:
        curve3 = plot.plot(pen=(255, 0, 0))
        curves_vz.append(curve3)
        last = data_vz[-1]
        data_vz = np.empty((chunkSize + 1, 2))
        data_vz[0] = last
        while len(curves_vz) > maxChunks:
            c = curves_vz.pop(0)
            plot.removeItem(c)
    else:
        curve3 = curves_vz[-1]
    data_vz[i + 1, 0] = now - startTime
    data_vz[i + 1, 1] = drone.navdata.demo.vz
    curve3.setData(x=data_vz[:i + 2, 0], y=data_vz[:i + 2, 1])
    ptr_vz += 1


def update():
    update_plot_vx()
    update_plot_vy()
    update_plot_vz()


