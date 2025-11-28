import math
import random
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
import cv2
from PIL import Image, ImageDraw, ImageFont


class TSquare(Drawer):

    @staticmethod
    def num_to_color(num):
        return (255 if num%3==0 else 0, 255 if num%3==1 else 0, 255 if num%3==2 else 0)

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, max_iterations=10):
        super().__init__(size, length, rate, field_size, border)
        self.max_iterations=max_iterations
        self.points=[]
        self.radius = min(self.field.x,self.field.y)*0.4
        first_point=Coords2D(self.field.x*0.3,self.field.y*0.7)
        second_point = first_point+Coords2D(0,-self.radius)
        third_point = first_point+Coords2D(self.radius,-self.radius)
        fourth_point = first_point+Coords2D(self.radius,0)
        self.points.extend([first_point,second_point,third_point,fourth_point])

    def get_all_states(self):
        #bc sometimes player skips first second???
        self.states.append({"points":deepcopy(self.points),"current_field_size":self.field})
        self.states.append({"points": deepcopy(self.points), "current_field_size": self.field})
        self.iter_points=deepcopy(self.points)

        for i in range(0, self.max_iterations):

            self.states.append(deepcopy(self.next_state()))

    def next_state(self):
        self.time+=1
        self.radius=self.radius/2
        new_iter_points=[]

        for p in self.iter_points:
            first_point = Coords2D(p.x-self.radius/2,p.y+self.radius/2)
            second_point = first_point + Coords2D(0, -self.radius)
            third_point = first_point + Coords2D(self.radius, -self.radius)
            fourth_point = first_point + Coords2D(self.radius, 0)
            new_iter_points.extend([first_point, second_point, third_point, fourth_point])

        self.points.extend(new_iter_points)
        self.iter_points=deepcopy(new_iter_points)
        return {"points":deepcopy(self.points),"current_field_size":self.field}

    def compute_scale(self, size,field_size):
        self.multiplier = min((size.x - self.border_width * 2) / field_size.x,
                              (size.y - self.border_width * 2) / field_size.y)
        self.offset.x = (size.x - field_size.x * self.multiplier) / 2
        self.offset.y = (size.y - field_size.y * self.multiplier) / 2


    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.compute_scale(size,state["current_field_size"])
        #self.grid(draw)
        #self.compute_scale(size, self.field) #resize once and for all?
        for i in range(0, math.floor(len(state["points"])/4)):
            #print("DRAWING: {0} to {1}".format(state[i],state[i+1]))
            draw.polygon([(self.offset.x+v.x*self.multiplier,self.offset.y+v.y*self.multiplier) for v in state["points"][(4*i):(4*(i+1))]], outline=(43,44,90), fill=(43,44,90), width=2)

        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img

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

