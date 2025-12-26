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

class ShrinkingWallDrawer(Drawer):

    def __init__(self, size=Coords2D(1920, 800), length=60, field_size=Coords2D(100,100), rate=1, border=False, acceleration=0):
        super().__init__(size, length, rate, field_size, border)
        self.circles=[]
        self.iter_no=0
        self.time_unit=1.0/rate
        self.multiplier=None
        self.acceleration=acceleration
        self.wall_field=deepcopy(self.field)
        self.wall_box =(0,0,self.field.x,self.field.y)
        self.walls=[
            Wall(Coords2D(0,0),Coords2D(self.field.x,0)),
            Wall(Coords2D(self.field.x,0), Coords2D(self.field.x, self.field.y)),
            Wall(Coords2D(self.field.x, self.field.y), Coords2D(0, self.field.y)),
            Wall(Coords2D(0, self.field.y), Coords2D(0, 0))
        ]
        self.ball=Ball(random.randint(15,20),Coords2D(random.randint(0,self.field.x),random.randint(0,self.field.y)),self.acceleration)

    def get_all_states(self):
        for cadre in range(0, self.length*self.rate):
            if (self.ball.radius > self.wall_field.x / 2):
                break
            self.states.append(deepcopy(self.next_state()))

    def next_state(self):

        #self.ball.change_size(0.3)
        for w in self.walls:
            w.resize(1)
            w.diminish(1)
        self.wall_field=Coords2D(max(w.start.x for w in self.walls)-min(w.start.x for w in self.walls),max(w.start.y for w in self.walls)-min(w.start.y for w in self.walls))
        self.wall_box=(min(w.start.x for w in self.walls),min(w.start.y for w in self.walls),
                       max(w.start.x for w in self.walls),max(w.start.y for w in self.walls))
        self.ball.step(self.time_unit,self.walls)
        self.time+=self.time_unit
        state={"iter_no":0,"walls":[]}
        self.circles.append({"center":self.ball.current_point,"radius":self.ball.radius,"color":self.ball.color,"wall_box":deepcopy(self.wall_box)})
        state["iter_no"]=deepcopy(self.iter_no)
        self.iter_no+=1
        for w in self.walls:
            state["walls"].append(deepcopy(w))
        return state

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        self.compute_scale(size)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        curr_wall_box = self.circles[state["iter_no"]-1]["wall_box"]
        for i in range(state["iter_no"]):
            b = self.circles[i]
            #if 0<=b.current_point.x-b.radius and b.current_point.x+b.radius<=self.field.x and 0<=b.current_point.y-b.radius and b.current_point.y+b.radius<=self.field.y:
            offset_current=self.offset_point(b["center"])
            print("Wall box is between: {0},{1} --- {2},{3}".format(curr_wall_box[0],curr_wall_box[1],curr_wall_box[2],curr_wall_box[3]))
            '''drawable_flg = Coords2D.exists_between(b["center"],curr_wall_box)
            for w in state["walls"]:
                drawable_flg = drawable_flg and (Coords2D.point_line_distance(b["center"],w.start,w.end)>=b["radius"])
            if ( drawable_flg ):'''
            if (True):
                draw.circle((offset_current.x,offset_current.y),b["radius"]*self.multiplier,fill=b["color"],outline="black",width=5)

        for w in state["walls"]:
            w_resized = (self.offset_point(w.start),self.offset_point(w.end))
            draw.line((w_resized[0].x,w_resized[0].y,w_resized[1].x,w_resized[1].y), fill="darkgrey", width=5)
        #if (self.border):
        #    self.draw_border(draw)
        self.watermark(draw)

        return img