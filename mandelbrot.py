from PIL import Image
from PIL import ImageDraw
from PIL import Image
from area import Area
import math
import numpy as np


class MandelImage:
    ITERATIONS = 50

    def __init__(self, size=(5000, 5000)):
        self.size = size
        self.im = Image.new('RGB', self.size)
        self.area = Area((-2, 2), 4, 4, 5000, 5000)

    def _get_mandel_points(self):
        self.area.mandelbrot()
        self.area.transform(mandelbrot=True)
        self.area.mandelbrot_points *= self.size[0]/4
        self.area.mandelbrot_points = self.area.mandelbrot_points.astype(np.int)
        for point in self.area.mandelbrot_points:
            yield point

    def drawMandel(self):
        d = ImageDraw.Draw(self.im)
        i = 0
        for point in self._get_mandel_points():
            d.point(list(point))
            i += 1
        self.im.save('test.png')
        print(i)

    @staticmethod
    def check_point(p):
        z = 0+0j
        for i in range(MandelImage.ITERATIONS):
            z = z**2 + p
            if abs(z) > 2 or (math.isnan(z.real) and math.isnan(z.imag)):
                return False
        return True
