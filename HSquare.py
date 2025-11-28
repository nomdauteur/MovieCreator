from TSquare import TSquare

import math
import random
from copy import deepcopy
from Coords2D import Coords2D
import cv2
from PIL import Image, ImageDraw, ImageFont


class HSquare(TSquare):

    def num_to_color(num):
        return (255 if num%3==0 else 0, 255 if num%3==1 else 0, 255 if num%3==2 else 0)

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,
                 max_iterations=10):
        super().__init__(size, length, rate, field_size, border,max_iterations)

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.compute_scale(size,state["current_field_size"])
        self.grid(draw)
        #self.compute_scale(size, self.field) #resize once and for all?
        for i in range(0, math.floor(len(state["points"])/4)):
            #print("DRAWING: {0} to {1}".format(state[i],state[i+1]))
            one,two,three,four=state["points"][(4*i):(4*(i+1))]
            middle_left=Coords2D.point_between(one,two,1/2)
            middle_right = Coords2D.point_between(three, four, 1 / 2)
            draw.line([self.offset.x + one.x * self.multiplier,
                       self.offset.y+ one.y*self.multiplier,
                       self.offset.x + two.x * self.multiplier,
                       self.offset.y + two.y * self.multiplier], fill=HSquare.num_to_color(i), width=5)
            draw.line([self.offset.x + three.x * self.multiplier,
                       self.offset.y + three.y * self.multiplier,
                       self.offset.x + four.x * self.multiplier,
                       self.offset.y + four.y * self.multiplier], fill=HSquare.num_to_color(i), width=5)
            draw.line([self.offset.x + middle_left.x * self.multiplier,
                       self.offset.y + middle_left.y * self.multiplier,
                       self.offset.x + middle_right.x * self.multiplier,
                       self.offset.y + middle_right.y * self.multiplier], fill=HSquare.num_to_color(i), width=5)

        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img


