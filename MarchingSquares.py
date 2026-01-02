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

class MarchingSquares(Drawer):

    def __init__(self, size=Coords2D(1920, 800), length=60, field_size=Coords2D(100,100), rate=1, border=False, side=100, base_color="blue", line_color="red"):
        super().__init__(size, length, rate, field_size, border)
        self.multiplier=None
        self.side = side
        self.base_color = base_color
        self.line_color = line_color
        self.numbers = [[0 for _ in range(self.side+1)] for _ in range(self.side+1)]
        self.indices = [[0 for _ in range(self.side)] for _ in range(self.side)]

        self.threshold = side*0.8
        self.small_grid=[[random.randint(-side,side) for j in range(math.ceil(self.side)+1)] for i in range(math.ceil(self.side)+1)]
        self.numbers = [[self.small_grid[math.floor(i/random.randint(1,5))][math.floor(j/random.randint(1,5))]+random.randint(-10,10) for j in range(self.side+1)] for i in range(self.side+1)]
        self.delta = 5
        print("Threshold: {0}".format(self.threshold))
        print(self.numbers)

    def get_all_states(self):
        for cadre in range(0, self.length*self.rate):
            #print("Forming {0}th state".format(cadre))
            self.states.append(deepcopy(self.next_state()))

    def count_indices(self):
        binary_matrix=[[1 if a > self.threshold else 0 for a in b] for b in self.numbers]
        for i in range(self.side):
            for j in range(self.side ):
                self.indices[i][j] = binary_matrix[i][j]*8+binary_matrix[i][j+1]*4+binary_matrix[i+1][j+1]*2+binary_matrix[i+1][j]


    def next_state(self):
        self.count_indices()
        #print("Indices are: {0}".format(self.indices))

        state = [[self.lookup(i,j) for j in range(self.side)] for i in range(self.side)]
        self.numbers=[[a+random.uniform(self.delta/2,self.delta) for a in b] for b in self.numbers]
        return state


    def lookup(self,i,j):
        top_left = Coords2D(j,i) #later scale to minisquare side and to multiplier; now treat small square as 1
        top_right = Coords2D(j+1,i)
        bottom_left = Coords2D(j,i+1)
        bottom_right = Coords2D(j+1,i+1)
        c = self.threshold
        left_wall_divide=(self.numbers[i][j]-c)/(self.numbers[i][j]-self.numbers[i+1][j]) if (self.numbers[i][j]-self.numbers[i+1][j]!=0) else 0
        right_wall_divide = (self.numbers[i][j+1]-c) / (self.numbers[i][j+1]-self.numbers[i+1][j+1]) if (self.numbers[i][j+1]-self.numbers[i+1][j+1]!=0) else 0
        top_wall_divide = (self.numbers[i][j]-c) / (self.numbers[i][j]-self.numbers[i][j+1]) if (self.numbers[i][j]-self.numbers[i][j+1]!=0) else 0
        bottom_wall_divide = (self.numbers[i + 1][j]-c) / (self.numbers[i + 1][j]-self.numbers[i+1][j+1]) if (self.numbers[i+1][j]-self.numbers[i+1][j+1]!=0) else 0

        '''left_wall_divide = 1/2
        right_wall_divide = 1/2
        top_wall_divide = 1/2
        bottom_wall_divide = 1/2'''

        match self.indices[i][j]:
            case 0 | 15:
                return []
            case 1 | 14:
                return [(Coords2D.point_between(top_left,bottom_left,left_wall_divide),
                         Coords2D.point_between(bottom_left,bottom_right,bottom_wall_divide))]
            case 2 | 13:
                return [(Coords2D.point_between(top_right, bottom_right, right_wall_divide),
                 Coords2D.point_between(bottom_left, bottom_right, bottom_wall_divide))]
            case 3 | 12:
                return [(Coords2D.point_between(top_left,bottom_left,left_wall_divide),
                         Coords2D.point_between(top_right, bottom_right, right_wall_divide))]
            case 4 | 11:
                return [(Coords2D.point_between(top_left, top_right, top_wall_divide),
                         Coords2D.point_between(top_right, bottom_right, right_wall_divide))]
            case 5:
                return [(Coords2D.point_between(top_left,bottom_left,left_wall_divide),
                         Coords2D.point_between(top_left, top_right, top_wall_divide)),
                        (Coords2D.point_between(top_right, bottom_right, right_wall_divide),
                         Coords2D.point_between(bottom_left, bottom_right, bottom_wall_divide))]
            case 10:
                return [(Coords2D.point_between(top_left, bottom_left, left_wall_divide),
                         Coords2D.point_between(bottom_left, bottom_right, bottom_wall_divide)),
                        (Coords2D.point_between(top_right, bottom_right, right_wall_divide),
                         Coords2D.point_between(top_left, top_right, top_wall_divide)
                         )]
            case 6|9:
                return [(Coords2D.point_between(top_left, top_right, top_wall_divide),
                 Coords2D.point_between(bottom_left, bottom_right, bottom_wall_divide))]
            case 7 | 8:
                return [(Coords2D.point_between(top_left, bottom_left, left_wall_divide),
                    Coords2D.point_between(top_left, top_right, top_wall_divide))]
            case _:
                return []


    def draw_image(self,state,size=None):
        square_side = self.field.x / self.side

        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        self.compute_scale(size)
        img = Image.new("RGB", (size.x,size.y), self.base_color)
        draw = ImageDraw.Draw(img)

        for i in range(self.side):
            for j in range(self.side):
                offset_lines = [(self.offset_point(l[0]*square_side).x,self.offset_point(l[0]*square_side).y,self.offset_point(l[1]*square_side).x,self.offset_point(l[1]*square_side).y) for l in state[i][j]]
                for l in offset_lines:
                    draw.line(l, fill=self.line_color, width=2)

        self.watermark(draw)

        #self.grid(draw)

        return img

    def grid(self,draw):
        square_side=self.field.x/self.side
        for i in range(self.side):
            draw.line([self.offset.x,
                           self.offset.y+i * square_side* self.multiplier,
                           self.offset.x + self.field.x * self.multiplier,
                           self.offset.y+i*square_side*self.multiplier], fill="lightcyan", width=2)

        for i in range(self.side):
            draw.line([self.offset.x +i *square_side* self.multiplier,
                       self.offset.y,
                           self.offset.x + i *square_side* self.multiplier,
                           self.offset.y+self.field.y*self.multiplier], fill="lightcyan", width=2)