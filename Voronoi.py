import math
import os


from Drawer import Drawer
from Coords2D import Coords2D
from Ball import Ball
from Wall import Wall
import random



from PIL import Image, ImageDraw, ImageFont
import numpy as np
import string
from copy import deepcopy

class Voronoi(Drawer):

    def __init__(self, size=Coords2D(1920, 800), length=60, field_size=Coords2D(100,100), rate=1, border=False, acceleration=0):
        super().__init__(size, length, rate, field_size, border)
        self.circles=[]
        self.iter_no=0
        self.time_unit=1.0/rate
        self.multiplier=None
        self.acceleration=acceleration
        self.walls=[
            Wall(Coords2D(0,0),Coords2D(self.field.x,0)),
            Wall(Coords2D(self.field.x,0), Coords2D(self.field.x, self.field.y)),
            Wall(Coords2D(self.field.x, self.field.y), Coords2D(0, self.field.y)),
            Wall(Coords2D(0, self.field.y), Coords2D(0, 0))
        ]
        self.balls=[Ball(5,Coords2D(random.randint(0,self.field.x),
                                                       random.randint(0,self.field.y)),self.acceleration,
                         Coords2D(random.randint(10,150),random.randint(10,150)))
                    for i in range(10)]

    def get_all_states(self):
        for cadre in range(0, self.length*self.rate):
            self.states.append(deepcopy(self.next_state()))

    def get_coloring(self):
        matrix = [[0 for i in range(self.field.x)] for j in range(self.field.y)]

        for i in range(self.field.y):
            for j in range(self.field.x):
                min_dist=(self.balls[0].current_point-Coords2D(j,i)).length()
                for b in range(1,len(self.balls)):
                    dist = (self.balls[b].current_point-Coords2D(j,i)).length()
                    if (dist < min_dist):
                        matrix[i][j] = b
                        min_dist = dist

        return matrix

    def next_state(self):
        state = {"iter_no": 0, "walls": []}
        state["iter_no"] = deepcopy(self.iter_no)
        state["balls"]=[]

        for b in self.balls:
            b.step(self.time_unit,self.walls,should_change_color=False)
            state["balls"].append({"center":b.current_point,"radius":b.radius,"color":b.color})
        self.time+=self.time_unit
        self.iter_no+=1

        state["color_matrix"]=self.get_coloring()

        return state

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        self.compute_scale(size)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        for i in range(self.field.y):
            for j in range(self.field.x):
                begin = self.offset_point(Coords2D(j, i))
                end = self.offset_point(Coords2D(j + 1, i + 1))
                ball_clr = state["balls"][state["color_matrix"][i][j]]["color"]
                clr = (min(ball_clr[0] +50, 255),
                       min(ball_clr[1] +50, 255),
                       min(ball_clr[2] +50, 255) )
                draw.rectangle((begin.x,begin.y,end.x,end.y), fill=clr)
        for b in state["balls"]:
            offset_current=self.offset_point(b["center"])
            draw.circle((offset_current.x,offset_current.y),b["radius"]*self.multiplier,fill=b["color"],outline="black",width=2)

        if (self.border):
            self.draw_border(draw)
        self.watermark(draw)

        return img

