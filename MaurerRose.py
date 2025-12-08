import math
import random
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
import cv2
from PIL import Image, ImageDraw, ImageFont


class MaurerRose(Drawer): #MonteCarlo, but not random (mostly for circular stuff, so go by phi)

    @staticmethod
    def num_to_color(num):
        return (255 if num%3==0 else 0, 255 if num%3==1 else 0, 255 if num%3==2 else 0)

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, need_grid=True
                 , n=2, d=30):
        super().__init__(size, length, rate, field_size, border)
        self.need_grid=need_grid
        self.phi=0
        self.n=n
        self.d=d
        self.stage=1 # 1 is rose, 2 is Maurer
        self.matrix = [[0 for _ in range(self.field.x)] for _ in range(self.field.y)]
        self.points=[]

    def rose_continue_condition(self):
        return (self.phi <=2*math.pi)


    def next_point(self,center,radius):
        point_real = (center +
                      Coords2D(radius * math.cos(self.phi) * math.sin(self.n * self.phi),
                               radius * math.sin(self.phi) * math.sin(self.n * self.phi)))
        point = Coords2D(math.floor(point_real.x), math.floor(point_real.y))
        return {"real":point_real,"int":point}

    def next_state(self):
        radius = self.field.x * 0.45
        center = Coords2D(self.field.x * 0.5, self.field.y * 0.5)

        if (self.stage==1):
            delta_phi=math.pi/180
            next_point=self.next_point(center,radius)
            self.matrix[next_point["int"].y][next_point["int"].x]=1
            self.phi+=delta_phi
            return deepcopy(self.matrix)
        else:
            next_point=(center+
                        Coords2D(radius*math.sin(self.n * self.d  * math.pi / 180.0 * self.point_no)*math.cos(self.d  * math.pi / 180.0 * self.point_no),
                                 radius*math.sin(self.n * self.d  * math.pi / 180.0 * self.point_no)*math.sin(self.d  * math.pi / 180.0 * self.point_no)))
            self.points.append(next_point)
            return deepcopy(self.points)



    def get_all_states(self):

        while (self.rose_continue_condition()):
            self.states.append({"state1":deepcopy(self.next_state()),"stage":self.stage})
        self.stage=2
        for i in range(0,361):
            self.point_no=i
            self.states.append({"state1":deepcopy(self.matrix),"state2":deepcopy(self.next_state()),"stage":self.stage})

    def compute_scale(self, size,field_size):
        self.multiplier = min((size.x - self.border_width * 2) / field_size.x,
                              (size.y - self.border_width * 2) / field_size.y)
        self.offset.x = (size.x - field_size.x * self.multiplier) / 2
        self.offset.y = (size.y - field_size.y * self.multiplier) / 2


    def draw_image(self,state,size=None):
        #print("Plus image")
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.compute_scale(size,self.field)
        if (self.need_grid):
            self.grid(draw)

        for i in range(self.field.y):
            for j in range(self.field.x):
                if (state["state1"][i][j] == 0):
                    continue
                draw.rectangle((self.offset.x+j*self.multiplier,self.offset.y+i*self.multiplier,self.offset.x+(j+1)*self.multiplier,self.offset.y+(i+1)*self.multiplier),fill="red")
        if (state["stage"] == 2):
            for i in range(0, len(state["state2"]) - 1):
                draw.line([self.offset.x + state["state2"][i].x * self.multiplier,
                           self.offset.y + state["state2"][i].y * self.multiplier,
                           self.offset.x + state["state2"][i + 1].x * self.multiplier,
                           self.offset.y + state["state2"][i + 1].y * self.multiplier], fill="blue", width=4)

        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img


    def grid(self,draw):
        for i in range(11):
            draw.line([self.offset.x,
                           self.offset.y+i *self.field.x/10 * self.multiplier,
                           self.offset.x + self.field.x *self.multiplier,
                           self.offset.y+i *self.field.x/10*self.multiplier], fill="lightcyan", width=2)

        for i in range(11):
            draw.line([self.offset.x +i  *self.field.x/10* self.multiplier,
                       self.offset.y,
                           self.offset.x + i  *self.field.x/10* self.multiplier,
                           self.offset.y+self.field.y *self.multiplier], fill="lightcyan", width=2)

