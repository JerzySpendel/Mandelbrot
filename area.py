import numpy as np


class Area:
    ITERATIONS = 50

    def __init__(self, LU, w, h, wx, wh):
        self.LU = LU
        self.space_x = np.linspace(LU[0], LU[0] + w, wx + 1)
        self.space_y = np.linspace(LU[1] - h, LU[1], wh + 1)
        self.w, self.h = w, h

    def points(self):
        return ([x, y] for x in self.space_x for y in self.space_y)

    def transform(self, mandelbrot=False):
        if not mandelbrot:
            for x in np.nditer(self.space_x, op_flags=['readwrite']):
                x += self.w/2
            for y in np.nditer(self.space_y, op_flags=['readwrite']):
                y += self.h/2
        else:
            print('ostro')
            if not hasattr(self, 'mandelbrot_points'):
                raise Exception('Area does not have defined mandelbrot points')
            for i in range(len(self.mandelbrot_points)):
                p = self.mandelbrot_points[i]
                self.mandelbrot_points[i] = [p[0] + self.w/2, p[1] + self.h/2]

    def point_in_mandelbrot(self, p):
        p = p[0] + p[1]*1j
        z = 0+0j
        for i in range(self.ITERATIONS):
            z = z**2 + p
            if abs(z) > 2:
                return False
        return True

    def points_in_mandelbrot(self):
        for point in self.points():
            if self.point_in_mandelbrot(point):
                yield point

    def mandelbrot(self):
        self.mandelbrot_points = np.array(list(self.points_in_mandelbrot()))
