import math
from PointyDraw import PointyDraw
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont

class Harmonograph(PointyDraw):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, need_grid=True,
                 a=[1,2,3,4],f=[1,2,3,4],p=[1,2,3,4],d=[1,2,3,4]):
        super().__init__(size, length, rate, field_size, border,need_grid)
        self.a=a
        self.f = f
        self.p = p
        self.d = d

    def continue_condition(self):
        return (self.f[0]*self.phi <=40*math.pi and self.f[0]!=0
                or self.f[1]*self.phi <=40*math.pi and self.f[1]!=0
                or self.f[2]*self.phi <=40*math.pi and self.f[2]!=0
                or self.f[3]*self.phi <=40*math.pi and self.f[3]!=0)

    def next_point(self,center,radius):
        print("Phi is: {0} pi".format(self.phi/math.pi))

        a_=[i*radius for i in self.a]

        point_real = center + Coords2D(
            a_[0]*math.sin(self.phi*self.f[0]+self.p[0])*math.exp(-self.d[0]*self.phi)+
            a_[1]*math.sin(self.phi*self.f[1]+self.p[1])*math.exp(-self.d[1]*self.phi),
            a_[2] * math.sin(self.phi * self.f[2] + self.p[2]) * math.exp(-self.d[2] * self.phi) +
            a_[3] * math.sin(self.phi * self.f[3] + self.p[3]) * math.exp(-self.d[3] * self.phi)
        )
        point = Coords2D(math.floor(point_real.x), math.floor(point_real.y))
        return {"real":point_real,"int":point}

    def draw_image(self, state, size=None):
        # print("Plus image")
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x, size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.compute_scale(size, self.field)
        if (self.need_grid):
            self.grid(draw)
        # self.compute_scale(size, self.field) #resize once and for all?
        for i in range(state-1):
            p_offset=self.offset_point(self.points[i])
            p_end_offset = self.offset_point(self.points[i+1])
            draw.line((p_offset.x,p_offset.y,p_end_offset.x,p_end_offset.y), width=2, fill="black")

        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img



