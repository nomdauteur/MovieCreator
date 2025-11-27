from copy import deepcopy
import random

from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D
import math
import cv2
from PIL import Image, ImageDraw, ImageFont


class Cesaro(PolyLineDrawer):

    def __init__(self,size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100),
                 border=False, max_iterations=0):
        super().__init__(size, length, rate, field_size, border)
        self.poly_lines=[]
        self.max_iterations=max_iterations
        self.iter_no=0
        #here be different variations
        """A= Coords2D(4/20,16/20)
        B = Coords2D(4/20, 4/20)
        C = Coords2D(16/20, 4/20)
        D=Coords2D(16/20,16/20)


        self.poly_lines.append(A)
        self.poly_lines.append(B)
        self.poly_lines.append(C)
        self.poly_lines.append(D)"""

        A = Coords2D(1 / 10, 14 / 20)
        C = Coords2D(18 / 20, 14 / 20)
        middle = Coords2D.point_between(A, C, 1 / 2)
        B = Coords2D.turn((middle - A)/math.cos(math.pi*15/90), math.pi / 2) + middle
        self.poly_lines.append(A)
        self.poly_lines.append(B)
        self.poly_lines.append(C)


    def get_all_states(self):
        #bc sometimes player skips first second???
        self.states.append({"lines":self.poly_lines,"current_field_size":self.field})
        self.states.append({"lines": self.poly_lines, "current_field_size": self.field})

        for i in range(0, self.max_iterations):

            self.states.append(deepcopy(self.next_state()))


    def next_state(self):
        self.iter_no+=1
        new_poly_lines=[]
        for i in range (len(self.poly_lines)-1):
            first_point=self.poly_lines[i]
            fifth_point=self.poly_lines[i+1]
            second_point=Coords2D.point_between(first_point,fifth_point,4/10)
            middle = Coords2D.point_between(first_point, fifth_point, 1 / 2)
            rotable_vector=(second_point-first_point)*math.tan(math.pi*17/90)*0.9
            third_point=middle + Coords2D.turn(rotable_vector,-math.pi/2)
            fourth_point=Coords2D.point_between(first_point,fifth_point,6/10)
            new_poly_lines.extend([first_point,second_point,third_point,fourth_point,fifth_point])
        #last line
        first_point = self.poly_lines[-1]
        fifth_point = self.poly_lines[0]
        second_point = Coords2D.point_between(first_point, fifth_point, 4 / 10)
        middle = Coords2D.point_between(first_point, fifth_point, 1 / 2)
        rotable_vector = (second_point - first_point) * math.tan(math.pi * 17 / 90)*0.9
        third_point = middle + Coords2D.turn(rotable_vector, -math.pi / 2)
        fourth_point = Coords2D.point_between(first_point, fifth_point, 6 / 10)
        new_poly_lines.extend([first_point, second_point, third_point, fourth_point, fifth_point])
        self.poly_lines=new_poly_lines
        return {"lines":self.poly_lines,"current_field_size":self.field}

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.compute_scale(size,state["current_field_size"])
        #self.compute_scale(size, self.field) #resize once and for all?

        #reflect

        to_draw1=[(self.offset.x+(v.x*self.field.x)*self.multiplier,
                               self.offset.y+((v.y-4/20)*self.field.y)*self.multiplier) for v in state["lines"]]

        to_draw2 = [(self.offset.x + (v.x * self.field.x) * self.multiplier,
                     self.offset.y - ((v.y-24/20) * self.field.y) * self.multiplier) for v in state["lines"]]
        #to_draw.append((self.offset.x+(state["lines"][0].x*self.field.x)*self.multiplier,self.offset.y+(state["lines"][0].y*self.field.y)*self.multiplier))

        draw.polygon(to_draw1, fill="green", outline="black", width=10 if self.iter_no<3 else 5 if self.iter_no<6
        else 3 if self.iter_no<8 else 2 if self.iter_no<10 else 1)
        draw.polygon(to_draw2, fill="green", outline="black", width=10 if self.iter_no < 3 else 5 if self.iter_no < 6
        else 3 if self.iter_no < 8 else 2 if self.iter_no < 10 else 1)
        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img
