
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

        self.nsteps = 1
        self.ypoints = range(-20, 22, self.nsteps)
        self.xpoints = range(-20, 22, self.nsteps)
        self.nfaces = len(self.ypoints)

        verts = np.array([
            [
                x, y, 0
            ] for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        faces = []
        colors = []

        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces

            for n in range(self.nfaces - 1):
                faces.append([n + yoff, yoff + n + self.nfaces,
                              yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n +  self.nfaces + 1])
                colors.append([0, 0, 0, 0])


        faces = np.array(faces)
        colors = np.array(colors)

        self.mesh1 = gl.GLMeshItem(
            vertexes=verts,
            faces=faces,
            faceColors=colors,
            smooth=False,
            drawEdges=True
        )

        self.mesh1.setGLOptions('additive')

        self.window.addItem(self.mesh1)


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()



if __name__ == '__main__':
    t = Terrain()
    t.start()

