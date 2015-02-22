from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo
import numpy as np
import numpy.random as rdn
import area
import sys


class MandelbrotWidget(QGLWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        # data = np.array(.2*rdn.randn(100000,2),dtype=np.float32)
        # data = np.array([[0,0], [0.5,0.5], [-0.5, -0.5]]).astype(np.float32)
        a = area.Area((-2, 2), 4, 4, 500, 500)
        r = a.opencl_mandelbrot()
        r = r[r[:,2] == 1,:]
        data = r[:,[0,1]]
        self.set_data(data)

    def set_data(self, data):
        self.data = data
        self.count = data.shape[0]

    def initializeGL(self):
        gl.glClearColor(0,0,0,0)
        self.vbo = glvbo.VBO(self.data)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glColor(1, 1, 0)
        self.vbo.bind()
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, self.vbo)
        gl.glDrawArrays(gl.GL_POINTS, 0, self.count)

    def resizeGL(self, width, height):
        gl.glViewport(0,0,width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-2, 2, -2, 2, -1, 1)


    def resizeEvent(self, event):
        w = self.width()
        h = self.height()
        self.resizeGL(w, h)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.central = QWidget()
        self.right = QWidget()
        self.mandel = MandelbrotWidget()
        self.right.setLayout(QVBoxLayout())
        self.setCentralWidget(self.central)
        self.resize(700, 500)
        self._set_central_mandelbrot()
        self._set_buttons()
        self.setWindowTitle('Test')

    def _set_central_mandelbrot(self):
        self.central.setLayout(QHBoxLayout())
        self.central.layout().addWidget(self.mandel)
        self.central.layout().addWidget(self.right)
        self.right.layout().addWidget(QPushButton("test"))

    def _set_buttons(self):
        self.refresh = QPushButton("Refresh")
        self.refresh.clicked.connect(self.mandel.repaint)
        self.right.layout().addWidget(self.refresh)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
