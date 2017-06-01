
import pyqtgraph as pg
import time

plt = pg.plot()

def update(data):
    plt.plot(data, clear=True)

class Thread(pg.QtCore.QThread):
    newData = pg.QtCore.Signal(object)
    def run(self):
        while True:
            data = pg.np.random.normal(size=100)
            # do NOT plot data from here!
            self.newData.emit(data)
            time.sleep(0.05)

thread = Thread()
thread.newData.connect(update)
thread.start()