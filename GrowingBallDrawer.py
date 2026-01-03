import math
import os

import subprocess

from Drawer import Drawer
from Coords2D import Coords2D
from Ball import Ball
from Wall import Wall
import random

from mingus.containers.note import Note
from mingus.containers.note_container import NoteContainer
from mingus.containers.bar import Bar
from mingus.containers.track import Track
import mingus.midi.midi_file_out as midi_file_out
from moviepy import VideoFileClip, AudioFileClip

import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import string
from copy import deepcopy

class GrowingBallDrawer(Drawer):

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
        self.ball=Ball(random.randint(5,20),Coords2D(random.randint(0,self.field.x),random.randint(0,self.field.y)),self.acceleration)

    def get_all_states(self):
        for cadre in range(0, self.length*self.rate):
            if (self.ball.radius > self.field.x / 2):
                break
            self.states.append(deepcopy(self.next_state()))

    def next_state(self):

        self.ball.change_size(0.3)
        step = self.ball.step(self.time_unit,self.walls)
        self.time+=self.time_unit
        state={"iter_no":0,"walls":[]}
        if step["collision"]:
            state["collided"]=step["collision_point"]
        else:
            state["collided"]=None
        self.circles.append({"center":self.ball.current_point,"radius":self.ball.radius,"color":self.ball.color})
        state["iter_no"]=deepcopy(self.iter_no)
        self.iter_no+=1
        for w in self.walls:
            state["walls"].append(w)
        return state

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        self.compute_scale(size)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        for i in range(state["iter_no"]):
            b = self.circles[i]
            #if 0<=b.current_point.x-b.radius and b.current_point.x+b.radius<=self.field.x and 0<=b.current_point.y-b.radius and b.current_point.y+b.radius<=self.field.y:
            offset_current=self.offset_point(b["center"])
            draw.circle((offset_current.x,offset_current.y),b["radius"]*self.multiplier,fill=b["color"],outline="black",width=5)

        if (self.border):
            self.draw_border(draw)
        self.watermark(draw)

        return img

    def get_note_container(self,state):
        if state["collided"] is None:
            return None
        c = Note()
        c.from_int(state["iter_no"] % 60)
        return c


