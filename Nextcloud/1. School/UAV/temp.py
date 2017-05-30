# -*- coding: utf-8 -*-
"""
Simple demonstration of TableWidget, which is an extension of QTableWidget
that automatically displays a variety of tabluar data formats.
"""

from pyardrone import ARDrone, at

drone = ARDrone()
drone.send(at.CONFIG('general:navdata_demo', True))
drone.emergency()
print("send")
drone.navdata_ready.wait()
print(drone.navdata_ready.wait())
drone.takeoff()
print("go")



import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

app = QtGui.QApplication([])

w = pg.TableWidget()
w.show()
w.resize(500, 500)
w.setWindowTitle('pyqtgraph example: TableWidget')

def update():
    data = np.array([
        (drone.navdata.demo.vx, 'vx'),
        (drone.navdata.demo.vy, 'vy'),
        (drone.navdata.demo.vx, 'vz'),
        (drone.navdata.demo.altitude, 'Hoogte'),
        (drone.navdata.demo.theta, 'Theta'),
        (drone.navdata.demo.phi, 'Phi'),
        (drone.navdata.demo.psi, 'Psi'),
    ], dtype=[('Column 1', float), ('Column 2', object)])

    w.setData(data)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)
## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

drone.land()
