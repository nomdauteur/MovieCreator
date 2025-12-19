import math
from copy import deepcopy
import random
from PIL import Image, ImageDraw, ImageFont

from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D


class ChaosGame(PolyLineDrawer):

    @staticmethod
    def num_to_color(num):
        return (0,0,0)

    def init(self):
        self.center=Coords2D(self.field.x/2,self.field.y/2)
        if self.lyambda<1:
            self.radius=min(self.field.x*0.45,self.field.y*0.45)
        else:
            self.radius=min(self.field.x*0.22,self.field.y*0.22)


    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,need_grid=False
                 , vertices_no=5, lyambda = 0.5, can_repeat=True):
        super().__init__(size, length, rate, field_size, border,need_grid)
        self.lyambda = lyambda
        self.init()
        self.vertices_no=vertices_no
        self.vertices=Coords2D.make_regular_polygon(self.vertices_no,self.center,self.radius)
        self.points=[self.center]

        self.can_repeat=can_repeat
        self.prev_vert=None
        self.iter_no=0



    def get_all_states(self):
        for i in range(12000):
            if (i%100==0):
                print("State no {0} generating".format(i))
            self.states.append(deepcopy(self.next_state()))


    def next_state(self):
        vertex_i= random.randint(0,len(self.vertices)-1)
        if self.can_repeat==False:
            if self.prev_vert is not None and self.prev_vert==vertex_i:
                vertex_i=(vertex_i+1)%len(self.vertices)
        current_point= self.points[-1]
        new_point=Coords2D.point_between(current_point,self.vertices[vertex_i],self.lyambda)
        self.points.append(new_point)
        self.prev_vert=vertex_i
        self.iter_no = self.iter_no+1
        return deepcopy(self.iter_no)

    def offset_point(self,point):
        return Coords2D(self.offset.x,self.offset.y)+point*self.multiplier

    def compute_scale(self, size):
        self.multiplier = min((size.x - self.border_width * 2) / self.field.x,
                              (size.y - self.border_width * 2) / self.field.y)
        self.offset.x = (size.x - self.field.x * self.multiplier) / 2
        self.offset.y = (size.y - self.field.y * self.multiplier) / 2

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.compute_scale(size)
        vertices_to_draw=[self.offset_point(v) for v in self.vertices]
        draw.polygon([(v.x,v.y) for v in vertices_to_draw], fill='white', outline='black', width=5)
        for i in range(state):
            p=self.points[i]
            p_offset=self.offset_point(p)
            p_end_offset=self.offset_point(p+Coords2D(1,1))
            draw.rectangle((p_offset.x,p_offset.y,p_end_offset.x,p_end_offset.y),fill='red')
        if (self.border):
            self.draw_border(draw)
        self.watermark(draw)

        return img