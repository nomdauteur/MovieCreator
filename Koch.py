from copy import deepcopy
import random

from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D
import math
import cv2
from PIL import Image, ImageDraw, ImageFont


class Koch(PolyLineDrawer):

    def __init__(self,size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100),
                 border=False, side=2, max_iterations=0):
        super().__init__(size, length, rate, field_size, border)
        self.side=side
        self.poly_lines=[]
        self.max_iterations=max_iterations
        self.iter_no=0

        A= Coords2D(1/10,14/20)
        C=Coords2D(18/20,14/20)
        B=Coords2D.turn(C-A,math.pi/3,A)
        self.poly_lines.append(A)
        self.poly_lines.append(B)
        self.poly_lines.append(C)


    def get_all_states(self):
        self.states.append({"lines":self.poly_lines,"current_field_size":self.field, "side":self.side})

        for i in range(0, self.max_iterations):

            self.states.append(deepcopy(self.next_state()))


    def next_state(self):
        new_poly_lines=[]
        for i in range (len(self.poly_lines)-1):
            first_point=self.poly_lines[i]
            fifth_point=self.poly_lines[i+1]
            second_point=Coords2D.point_between(first_point,fifth_point,1/3)
            rotable_vector=second_point-first_point
            third_point=second_point + Coords2D.turn(rotable_vector,math.pi/3)
            fourth_point=Coords2D.point_between(first_point,fifth_point,2/3)
            new_poly_lines.extend([first_point,second_point,third_point,fourth_point,fifth_point])
        #last line
        first_point = self.poly_lines[-1]
        fifth_point = self.poly_lines[0]
        second_point = Coords2D.point_between(first_point,fifth_point,1/3)
        rotable_vector = second_point - first_point
        third_point = second_point + Coords2D.turn(rotable_vector,math.pi/3)
        fourth_point = Coords2D.point_between(first_point,fifth_point,2/3)
        new_poly_lines.extend([first_point, second_point, third_point, fourth_point, fifth_point])
        self.poly_lines=new_poly_lines
        return {"lines":self.poly_lines,"current_field_size":self.field, "side":self.side}

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.compute_scale(size,state["current_field_size"])
        #self.compute_scale(size, self.field) #resize once and for all?
        side_x = self.field.x / state["side"]
        side_y = self.field.y / state["side"]

        for i in range(state["side"]):
            for j in range(state["side"]):
                offset_x = j * side_x
                offset_y = i * side_y
                to_draw=[(self.offset.x+(offset_x+v.x*side_x)*self.multiplier,
                               self.offset.y+(offset_y+v.y*side_y)*self.multiplier) for v in state["lines"]]

                draw.polygon(to_draw, outline="black", fill="yellow" if (i+j)%2==0 else (0, 100, 0), width=2)


        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img
