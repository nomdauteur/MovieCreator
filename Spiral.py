import math
from copy import deepcopy
import random

from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D


class Spiral(PolyLineDrawer):

    @staticmethod
    def num_to_color(num):
        return (0,0,0)

    def init_config(self):
        self.lyambda=0.1
        self.epsilon=1
        self.init_vertices=4
        self.radius = min(self.field.x, self.field.y) * 0.9
        first_point = Coords2D(self.field.x * 0.05, self.field.y * 0.95)
        second_point = first_point + Coords2D(0, -self.radius)
        third_point = first_point + Coords2D(self.radius, -self.radius)
        fourth_point = first_point + Coords2D(self.radius, 0)
        self.poly_lines=[first_point,second_point,third_point,fourth_point,first_point]
        '''self.init_vertices = 3
        self.radius = min(self.field.x, self.field.y) * 0.9
        first_point = Coords2D(self.field.x * 0.05, self.field.y * 0.85)
        third_point = first_point + Coords2D(self.radius, 0)
        second_point=Coords2D.turn(third_point-first_point,math.pi/3,first_point)
        self.poly_lines = [first_point, second_point, third_point, first_point]'''

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False):
        super().__init__(size, length, rate, field_size, border)
        self.init_config()

    def last_length(self):
        return (self.poly_lines[-1]-self.poly_lines[-2]).length()


    def get_all_states(self): #not by hard time but by ending of figure
        while(self.last_length()>self.epsilon):
            print((self.poly_lines[-1]-self.poly_lines[-2]).length())
            self.states.append(deepcopy(self.next_state()))

    def next_state(self):
        off=random.uniform(-self.lyambda/10,self.lyambda/10)
        self.poly_lines.append(Coords2D.point_between(self.poly_lines[-self.init_vertices],self.poly_lines[-self.init_vertices+1],self.lyambda+off))
        return {"lines": self.poly_lines, "current_field_size": self.field}