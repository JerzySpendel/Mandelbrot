import numpy as np
import cl
import pyopencl


class Area:
    ITERATIONS = 50

    def __init__(self, LU, w, h, wx, wh):
        self.LU = LU
        self.space_x = np.linspace(LU[0], LU[0] + w, wx + 1)
        self.space_y = np.linspace(LU[1] - h, LU[1], wh + 1)
        self.w, self.h = w, h
        self.prog = cl.prog

    @staticmethod
    def cartesian_product(a, b):
        return np.transpose([np.tile(a, len(b)), np.repeat(b, len(a))])

    def points(self):
        return ([x, y] for x in self.space_x for y in self.space_y)

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

    def opencl_mandelbrot(self):
        flags = pyopencl.mem_flags
        cartesian_product = Area.cartesian_product(self.space_x, self.space_y)
        area = np.hstack((cartesian_product, np.zeros((cartesian_product.shape[0], 2)))).astype(np.float32)
        a_buff = pyopencl.Buffer(cl.ctx, flags.READ_WRITE, size=area.nbytes)
        pyopencl.enqueue_write_buffer(cl.queue, a_buff, area)
        self.prog.calc(cl.queue, area.shape, None, a_buff)
        res = np.empty_like(area)
        pyopencl.enqueue_read_buffer(cl.queue, a_buff, res).wait()
        return res
