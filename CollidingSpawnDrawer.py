import math

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

class CollidingSpawnDrawer(Drawer):

    def __init__(self, size=Coords2D(1920, 800), length=60, field_size=Coords2D(100,100), rate=1, border=False, acceleration=0):
        super().__init__(size, length, rate, field_size, border)
        self.circles=[]
        self.iter_no=0
        self.wait_constant= 0.5
        self.last_collision_iter_no=-self.wait_constant
        self.collisions_count = 0
        self.time_unit=1.0/rate
        self.multiplier=None
        self.acceleration=acceleration
        self.walls=[
            Wall(Coords2D(0,0),Coords2D(self.field.x,0)),
            Wall(Coords2D(self.field.x,0), Coords2D(self.field.x, self.field.y)),
            Wall(Coords2D(self.field.x, self.field.y), Coords2D(0, self.field.y)),
            Wall(Coords2D(0, self.field.y), Coords2D(0, 0))
        ]
        self.balls=[Ball(random.randint(10,20),Coords2D(random.randint(0,self.field.x),random.randint(0,self.field.y)),self.acceleration),
                    Ball(random.randint(10, 20),
                         Coords2D(random.randint(0, self.field.x), random.randint(0, self.field.y)), self.acceleration)]

    def get_all_states(self):
        for cadre in range(0, self.length*self.rate):
            if (len(self.balls)>5000):
                break
            self.states.append(deepcopy(self.next_state()))

    @staticmethod
    def check_collision(ball1, ball2):
        distance = (ball2.current_point-ball1.current_point).length()
        if distance>(ball1.radius + ball2.radius):
            return {"collision":False,"new_center":None,"new_radius":None,"new_color":None}
        else:
            return {"collision": True,
                    "new_center": Coords2D.point_between(ball1.current_point,ball2.current_point,0.5),
                    "new_radius": (ball1.radius+ball2.radius)/2,
                    "new_color": (math.floor((ball1.color[0]+ball2.color[0])/2),
                                  math.floor((ball1.color[1]+ball2.color[1])/2),
                                  math.floor((ball1.color[2]+ball2.color[2])/2))
                        }

    def next_state(self):

        for b in self.balls:
            b.step(self.time_unit,self.walls)

        add_balls=[]
        for i in range(len(self.balls)):
            for j in range(len(self.balls)):
                if j<=i:
                    continue
                collision = CollidingSpawnDrawer.check_collision(self.balls[i],self.balls[j])
                #Give them a fraction of second not to spam overall
                if (collision["collision"] and self.iter_no-self.last_collision_iter_no>self.wait_constant):
                    print("Ball {0} collided to ball {1} on {2} iteration".format(i,j,self.iter_no))
                    add_balls.append(
                            Ball(collision["new_radius"],
                             collision["new_center"], self.acceleration,collision["new_color"])
                            )
                    self.last_collision_iter_no=self.iter_no


        self.balls.extend(add_balls)
        self.time+=self.time_unit
        state={"iter_no":0,"walls":[]}
        state["balls"]=deepcopy(self.balls)
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
        for b in state["balls"]:
            offset_current=self.offset_point(b.current_point)
            draw.circle((offset_current.x,offset_current.y),b.radius*self.multiplier,fill=b.color,outline="black",width=5)

        for w in state["walls"]:
            w_resized = (self.offset_point(w.start),self.offset_point(w.end))
            draw.line((w_resized[0].x,w_resized[0].y,w_resized[1].x,w_resized[1].y), fill="darkgrey", width=5)
        #if (self.border):
        #    self.draw_border(draw)
        self.watermark(draw)

        return img