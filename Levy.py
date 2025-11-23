from copy import deepcopy
import random

from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D
import math
import cv2
from PIL import Image, ImageDraw, ImageFont


class Levy(PolyLineDrawer):

    def __init__(self,size=Coords2D(1080,1920), length=60, rate=1, field_size=Coords2D(900, 1600),
                 border=False, max_iterations=10):
        super().__init__(size, length, rate, field_size, border)
        self.max_iterations = max_iterations
        self.poly_lines=[]

        A= Coords2D(self.field.x*0.3,self.field.y*0.3)
        B=Coords2D(self.field.x*0.3,self.field.y*0.7)
        self.poly_lines.append(A)
        self.poly_lines.append(B)

    def get_all_states(self):
        self.states.append({"lines":self.poly_lines,"current_field_size":self.field})
        print("Initial state:")
        for i in self.poly_lines:
            print(i)


        for i in range(0, self.max_iterations):

            self.states.append(deepcopy(self.next_state()))


    def next_state(self):
        new_poly_lines=[]
        for i in range (len(self.poly_lines)-1):
            first_point=self.poly_lines[i]
            third_point=self.poly_lines[i+1]
            middle=Coords2D.point_between(first_point,third_point,1/2)
            second_point=Coords2D.turn(middle-first_point,math.pi/2)+middle
            new_poly_lines.extend([first_point,second_point,third_point])

        self.poly_lines=new_poly_lines
        return {"lines":self.poly_lines,"current_field_size":self.field}

