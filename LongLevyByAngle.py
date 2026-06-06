import copy
from copy import deepcopy
import random

from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D
import math
import cv2
from PIL import Image, ImageDraw, ImageFont


class LongLevyByAngle(PolyLineDrawer):

    def __init__(self,size=Coords2D(1080,1920), length=60, rate=1, field_size=Coords2D(900, 1600),
                 border=False, max_iterations=10, verbose=False):
        super().__init__(size, length, rate, field_size, border)
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.init_poly_lines=[]

        A= Coords2D(self.field.x*0.37,self.field.y*0.5)
        B=Coords2D(self.field.x*0.63,self.field.y*0.5)
        self.init_poly_lines.append(A)
        self.init_poly_lines.append(B)

    def get_all_states(self):

        for i in range(0, 360,10):
            print("angle is {0}".format(i))
            self.curr_angle=i
            self.poly_lines = copy.deepcopy(self.init_poly_lines)

            self.states.append({"iter":0,"val":
                {"lines":deepcopy(self.poly_lines),"current_field_size":self.field, "angle":deepcopy(self.curr_angle)}})
            for i in range(self.max_iterations):
                self.iter_no=i
                self.states.append(deepcopy(self.next_state()))
        if not self.verbose:
            self.states = [s for s in self.states if s["iter"]==self.max_iterations-1]

    def next_state(self):
        return {"iter":deepcopy(self.iter_no),"val":deepcopy(self.next_lineage(self.curr_angle))}
        return l



    def next_lineage(self,angle):
        new_poly_lines=[]
        coeff=math.sin(angle * math.pi / 180)
        for i in range (len(self.poly_lines)-1):
            first_point=self.poly_lines[i]
            third_point=self.poly_lines[i+1]
            if first_point==Coords2D(-1,-1):
                new_poly_lines.append(first_point)
                continue
            if third_point==Coords2D(-1,-1):
                continue
            middle=Coords2D.point_between(first_point,third_point,1/2)
            second_point=Coords2D.turn((middle-first_point)*coeff,math.pi/2)+middle
            new_poly_lines.extend([first_point,second_point,third_point])

        self.poly_lines=new_poly_lines
        return {"lines":deepcopy(self.poly_lines),"current_field_size":self.field, "angle":deepcopy(self.curr_angle)}

    def draw_image(self, state, size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x, size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.compute_scale(size,self.field)
        #print(state)
        text_point = Coords2D(180, 200)
        font = ImageFont.truetype("segoesc.ttf", 20)
        draw.text((text_point.x, text_point.y),
                  "angle = " + str(state["val"]["angle"])+" degrees", font=font, fill="black")

        for i in range(len(state["val"]["lines"])-1):
            start = self.offset_point(state["val"]["lines"][i])
            end = self.offset_point(state["val"]["lines"][i+1])
            draw.line([start.x,start.y,end.x,end.y], fill=self.fill(i), width=8)



        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        #img.save("videos/"+"LevyAngle_"+".jpg")

        return img


