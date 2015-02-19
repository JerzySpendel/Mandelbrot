from PIL import Image
from PIL import ImageDraw
from PIL import Image
import math

class MandelImage:
    ITERATIONS = 50

    def __init__(self):
        self.size = (4000,4000)
        self.im = Image.new('RGB', self.size)

    def _get_mandel_points(self):
        ratio_x = self.size[0]/2
        ratio_y = self.size[1]/2
        points = []
        for (x, y) in [(x, y) for x in range(-self.size[0], self.size[0]) for y in range(-self.size[1], self.size[1])]:
            x, y = x/(self.size[0]/2), y/(self.size[1]/2)
            if MandelImage.check_point(x+y*1j): points.append(((self.size[0]/4)*(x+2), (self.size[1]/4)*(y+2)))
        return points

    def drawMandel(self):
        d = ImageDraw.Draw(self.im)
        d.point(self._get_mandel_points())
        self.im.save('test.png')

    @staticmethod
    def check_point(p):
        z = 0+0j
        for i in range(MandelImage.ITERATIONS):
            z = z**2 + p
        if math.isnan(z.real) and math.isnan(z.imag):
            return False
        return True
