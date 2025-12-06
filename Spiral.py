import math
from copy import deepcopy
import random

from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D


class Spiral(PolyLineDrawer):

    @staticmethod
    def num_to_color(num):
        return (0,0,0)

    def add_config(self,config, lyambda):
        self.lyambda=lyambda
        self.epsilon=self.field.x/12
        self.init_vertices =len(config)
        self.curr_poly_lines=deepcopy(config)
        self.curr_poly_lines.append(deepcopy(config[0]))
        self.poly_lines.extend(deepcopy(self.curr_poly_lines))
        self.get_states()

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,need_grid=False):
        super().__init__(size, length, rate, field_size, border,need_grid)
        #self.init_config()

    def last_length(self):
        return (self.poly_lines[-1]-self.poly_lines[-2]).length()


    def get_states(self): #not by hard time but by ending of figure
        while(self.last_length()>self.epsilon):
            print(self.last_length())
            self.states.append(deepcopy(self.next_state()))
        self.poly_lines.append(Coords2D(-1,-1))

    def get_all_states(self):
        return self.states

    def fill(self,number):
        return (0,0,0)
        modulo=number%self.init_vertices
        match modulo:
            case 0:
                return 'red'
            case 1:
                return 'green'
            case 2:
                return 'blue'
            case 3:
                return 'yellow'
            case 4:
                return 'purple'
            case 5:
                return 'pink'
            case 6:
                return 'gray'
            case 7:
                return 'black'

    def next_state(self):
        off=random.uniform(-self.lyambda/10,self.lyambda/10)
        self.poly_lines.append(Coords2D.point_between(self.poly_lines[-self.init_vertices],self.poly_lines[-self.init_vertices+1],self.lyambda+off))
        return {"lines": self.poly_lines, "current_field_size": self.field}