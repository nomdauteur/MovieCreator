from Drawer import Drawer
from Coords2D import Coords2D
from Ball import Ball
from Wall import Wall
import random

import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import string
from copy import deepcopy

class BallDrawer(Drawer):

    def __init__(self, size=Coords2D(1920, 800), length=60, field_size=Coords2D(100,100), rate=1, border=False, acceleration=0):
        super().__init__(size, length, rate, field_size, border)
        balls_count=random.randint(1,5)
        self.time_unit=1.0/rate
        self.multiplier=None
        self.acceleration=acceleration
        self.balls=[]
        self.walls=[
            Wall(Coords2D(0,0),Coords2D(self.field.x,0)),
            Wall(Coords2D(self.field.x,0), Coords2D(self.field.x, self.field.y)),
            Wall(Coords2D(self.field.x, self.field.y), Coords2D(0, self.field.y)),
            Wall(Coords2D(0, self.field.y), Coords2D(0, 0))
        ]
        for i in range(0,balls_count):
            self.balls.append(Ball(random.randint(5,20),Coords2D(random.randint(0,self.field.x),random.randint(0,self.field.y)),self.acceleration))


    def next_state(self):
        add_ball_flag=random.randint(0,3)
        if (add_ball_flag==1):
            self.balls.append(
                Ball(random.randint(5, 20), Coords2D(random.randint(0, self.field.x), random.randint(0, self.field.y)),self.acceleration))
        for ball in self.balls:
            ball.step(self.time_unit,self.walls)
        self.time+=self.time_unit
        state={"balls":[],"walls":[]}
        for b in self.balls:
            state["balls"].append(b)
        for w in self.walls:
            state["walls"].append(w)
        return state

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        self.compute_scale(size)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        for b in state["balls"]:
            if 0<=b.current_point.x-b.radius and b.current_point.x+b.radius<=self.field.x and 0<=b.current_point.y-b.radius and b.current_point.y+b.radius<=self.field.y:
                draw.circle((self.offset.x+b.current_point.x*self.multiplier,self.offset.y+b.current_point.y*self.multiplier),b.radius*self.multiplier,b.color)

        if (self.border):
            self.draw_border(draw)
        self.watermark(draw)

        return img