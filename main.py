
from pyqtgraph.Qt import QtCore, QtGui
from opensimplex import OpenSimplex
import pyqtgraph.opengl as gl

import numpy as np
import sys


class Terrain(object):

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.window = gl.GLViewWidget()
        self.window.setGeometry(0, 110, 1920, 1080)
        self.window.show()
        self.window.setWindowTitle('GL Mesh Terrain')
        self.window.setCameraPosition(distance=30, elevation=8)

        grid = gl.GLGridItem()
        grid.scale(2, 2, 2)

        self.window.addItem(grid)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()



if __name__ == '__main__':
    t = Terrain()
    t.start()
