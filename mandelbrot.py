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
        ep = self.equal_parts = 10
        x = self.x_coordinates = [2-(4/ep)*x for x in range(1, ep+1)]
        y = self.y_coordinates = [2-(4/ep)*x for x in range(1, ep+1)]
        self.xy_coordinates = [(x_, y_) for x_ in x for y_ in y]
        self.area = (Area((xy[0], xy[1]), 4/ep, 4/ep, size[0]/ep, size[1]/ep) for xy in self.xy_coordinates)

    def _get_mandel_points(self, return_array=False):
        i = 0
        for area in self.area:
            print(i)
            i += 1
            t = time.time()
            points = area.opencl_mandelbrot() # numpy array, not list
            print('Wygenerowano w', time.time() - t)
            points[:, [0, 1]] *= self.ratio*self.size[0]/4
            points[:, [0, 1]] += self.size[0]/2
            points = points[points[:,2]  != 0]
            points = points.astype(np.int32)
            for point in points:
                if point[2] == 1:
                    yield point[0], point[1]

    def drawMandel(self):
        d = ImageDraw.Draw(self.im)
        points_to_draw = []
        for point in self._get_mandel_points():
            points_to_draw.append(point) #sth like buffer
        for point in points_to_draw:
            d.point(point)
        self.im.save('test1.png')

    @staticmethod
    def check_point(p):
        z = 0+0j
        for i in range(MandelImage.ITERATIONS):
            z = z**2 + p
            if abs(z) > 2 or (math.isnan(z.real) and math.isnan(z.imag)):
                return False
        return True
