
from pyqtgraph.Qt import QtCore, QtGui
from opensimplex import OpenSimplex

import pyqtgraph.opengl as gl

import pyaudio
import struct

import numpy as np
import sys


class Terrain(object):

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.window = gl.GLViewWidget()
        self.window.setGeometry(0, 110, 1920, 1080)
        # self.window.setFixedSize(WidthOfParent, HeightOfParent)
        self.window.show()
        self.window.setWindowTitle('GL Mesh Terrain')
        self.window.setCameraPosition(distance=30, elevation=12)

        self.nsteps = 1.3
        self.offset = 0
        self.ypoints = np.arange(-20, 20 + self.nsteps, self.nsteps)
        self.xpoints = np.arange(-20, 20 + self.nsteps, self.nsteps)
        self.nfaces = len(self.ypoints)

        self.amp_mult = 2.5

        self.RATE = 44100
        self.CHUNK = len(self.xpoints) * len(self.ypoints)

        self.p = pyaudio.PyAudio()
        # self.stream = self.p.open(
        #     format=pyaudio.paInt16,
        #     channels=1,
        #     rate=self.RATE,
        #     input=True,
        #     output=True,
        #     frames_per_buffer=self.CHUNK,
        # )

        self.noise = OpenSimplex()

        verts, faces, colors = self.mesh()

        self.mesh1 = gl.GLMeshItem(
            vertexes=verts,
            faces=faces,
            faceColors=colors,
            smooth=False,
            drawEdges=True,
        )

        self.mesh1.setGLOptions('additive')

        self.window.addItem(self.mesh1)

    
    def mesh(self, offset=0, height=2.5, wf_data=None):

        if wf_data:

            wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
            wf_data = np.array(wf_data, dtype='b')[::2] + 128
            wf_data = np.array(wf_data, dtype='int32') - 128
            wf_data = wf_data * 0.04
            wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))

        else:
            wf_data = np.array([1] * 1024)
            wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))

        verts = np.array([
            [
                x, y, self.amp_mult * wf_data[xid][yid] * self.noise.noise2d(x=xid / 5 + offset, y=yid / 5 + offset)
            ] for xid, x in enumerate(self.xpoints) for yid, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        faces = []
        colors = []

        for yid in range(self.nfaces - 1):
            yoff = yid * self.nfaces

            for xid in range(self.nfaces - 1):
                faces.append([xid + yoff,
                              yoff + xid + self.nfaces,
                              yoff + xid + self.nfaces + 1])

                faces.append([xid + yoff,
                              yoff + xid + 1,
                              yoff + xid +  self.nfaces + 1])

                colors.append([xid / self.nfaces,
                               1 - xid / self.nfaces,
                               yid / self.nfaces, 0.7])

                colors.append([xid / self.nfaces,
                               1 - xid / self.nfaces,
                               yid / self.nfaces, 0.8])


        faces = np.array(faces)
        colors = np.array(colors)

        return verts, faces, colors


    def update(self):

        # wf_data = self.stream.read(self.CHUNK)

        # verts, faces, colors = self.mesh(offset=self.offset, wf_data=wf_data)
        verts, faces, colors = self.mesh(offset=self.offset)

        self.mesh1.setMeshData(
            vertexes=verts,
            faces=faces,
            faceColors=colors
        )

        self.offset -= 0.15


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            self.app.exec_()


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)

        self.start()
        self.update()


if __name__ == '__main__':
    t = Terrain()
    t.animation()

