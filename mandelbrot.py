from PIL import Image
from PIL import ImageDraw
from PIL import Image
from area import Area
import math
import time
import numpy as np


class MandelImage:
    ITERATIONS = 50

    def __init__(self, size=(500, 500)):
        self.size = size
        self.im = Image.new('RGB', self.size)
        self.ratio = 1
        self.area = Area((-2, 2), 4, 4, size[0], size[1])

    def _get_mandel_points(self):
        t = time.time()
        points = self.area.opencl_mandelbrot() # numpy array, not list
        print('Wgenerowano w', time.time() - t)
        points[:, [0, 1]] *= self.ratio*self.size[0]/4
        points[:, [0, 1]] += self.size[0]/2
        points = points.astype(np.int32)
        for point in points:
            if point[2] == 1:
                yield point[0], point[1]

    def drawMandel(self):
        d = ImageDraw.Draw(self.im)
        i = 0
        for point in self._get_mandel_points():
            d.point(point)
            i += 1
        self.im.save('test1.png')
        print(i)

    @staticmethod
    def check_point(p):
        z = 0+0j
        for i in range(MandelImage.ITERATIONS):
            z = z**2 + p
            if abs(z) > 2 or (math.isnan(z.real) and math.isnan(z.imag)):
                return False
        return True
