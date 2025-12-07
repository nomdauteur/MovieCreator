import math
import random
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
import cv2
from PIL import Image, ImageDraw, ImageFont


class MonteCarlo(Drawer):

    @staticmethod
    def num_to_color(num):
        return (255 if num%3==0 else 0, 255 if num%3==1 else 0, 255 if num%3==2 else 0)

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, need_grid=False):
        super().__init__(size, length, rate, field_size, border)
        self.need_grid=need_grid
        # -1 for check unmatch, 0 for uncheck, 1 for check match
        self.matrix=[[0 for _ in range(self.field.x)] for _ in range(self.field.y)]


    @staticmethod
    def matches(self,point): # will override
        # exemplary function: x2+y2=400 offset to (20,20)
        epsilon = self.field.x/10

        return (abs((point.x-20)*(point.x-20)+(point.y-20)*(point.y-20)-400)<=epsilon)

    def next_state(self):

        point = Coords2D(random.randint(0,self.field.x-1),random.randint(0,self.field.y-1))

        while(self.matrix[point.y][point.x]!=0):
            point = Coords2D(random.randint(0, self.field.x-1), random.randint(0, self.field.y-1))


        self.matrix[point.y][point.x]=1 if MonteCarlo.matches(self,point) else -1

        return deepcopy(self.matrix)

    def get_all_states(self):

        for i in range(0, self.field.x*self.field.y):
            self.states.append(deepcopy(self.next_state()))
            print("Iteration: {0}".format(i))

    def compute_scale(self, size,field_size):
        self.multiplier = min((size.x - self.border_width * 2) / field_size.x,
                              (size.y - self.border_width * 2) / field_size.y)
        self.offset.x = (size.x - field_size.x * self.multiplier) / 2
        self.offset.y = (size.y - field_size.y * self.multiplier) / 2


    def draw_image(self,state,size=None):
        print("Plus image")
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

