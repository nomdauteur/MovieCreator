import math
import random
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
import cv2
from PIL import Image, ImageDraw, ImageFont


class PointyDraw(Drawer): #MonteCarlo, but not random (mostly for circular stuff, so go by phi)

    @staticmethod
    def num_to_color(num):
        return (255 if num%3==0 else 0, 255 if num%3==1 else 0, 255 if num%3==2 else 0)

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, need_grid=False):
        super().__init__(size, length, rate, field_size, border)
        self.need_grid=need_grid
        self.phi=0
        # -1 for check unmatch, 0 for uncheck, 1 for check match
        self.matrix=[[0 for _ in range(self.field.x)] for _ in range(self.field.y)]


    '''@staticmethod
    def matches(self,point,center, radius): # will override
        # exemplary function: x2+y2=400 offset to (20,20)
        epsilon = self.field.x/10

        return (abs((point.x-center.x)*(point.x-center.x)+(point.y-center.y)*(point.y-center.y)-radius*radius)<=epsilon)
    '''
    def next_point(self,center,radius):
        point_real = center + Coords2D(radius * math.cos(self.phi), radius * math.sin(self.phi))
        point = Coords2D(math.floor(point_real.x), math.floor(point_real.y))
        return {"real":point_real,"int":point}

    def next_state(self):
        delta_phi=math.pi/180
        radius=self.field.x*0.45
        center=Coords2D(self.field.x*0.5,self.field.y*0.5)
        next_point=self.next_point(center,radius)
        #print(point)
        self.matrix[next_point["int"].y][next_point["int"].x]=1

        self.phi+=delta_phi

        return deepcopy(self.matrix)

    def continue_condition(self):
        return (self.phi <=2*math.pi)

    def get_all_states(self):

        while (self.continue_condition()):
            self.states.append(deepcopy(self.next_state()))
            #print("Iteration: {0} pi".format(self.phi/math.pi))

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
        #self.compute_scale(size, self.field) #resize once and for all?
        for i in range(self.field.y):
            for j in range(self.field.x):
                if (state[i][j] == 0):
                    continue
                if (state[i][j]==1):
                    color="black"
                if (self.matrix[i][j]==-1):
                    color="gray"
                draw.rectangle((self.offset.x+j*self.multiplier,self.offset.y+i*self.multiplier,self.offset.x+(j+1)*self.multiplier,self.offset.y+(i+1)*self.multiplier),fill=color)

        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img

    def fill(self,number):
        return PolyLineDrawer.num_to_color(number)

    def grid(self,draw):
        for i in range(self.field.y):
            draw.line([self.offset.x,
                           self.offset.y+i * self.multiplier,
                           self.offset.x + self.field.x * self.multiplier,
                           self.offset.y+i*self.multiplier], fill="lightcyan", width=2)

        for i in range(self.field.x):
            draw.line([self.offset.x +i * self.multiplier,
                       self.offset.y,
                           self.offset.x + i * self.multiplier,
                           self.offset.y+self.field.y*self.multiplier], fill="lightcyan", width=2)

