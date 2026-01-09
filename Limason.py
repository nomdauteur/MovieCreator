import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont

class Limason(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, center = Coords2D(50,50), radius = 40, point=Coords2D(100,100)):
        super().__init__(size, length, rate, field_size, border)
        self.iter_no=0
        self.center = center
        self.radius = radius
        self.point = point

        self.file_name = "videos/Limason_" + str(self.point.x)+"_" + str(self.point.y)+"_"

    def next_state(self):
        self.iter_no+=1
        return deepcopy(self.iter_no)

    def get_all_states(self):
        for i in range(120):
            self.states.append(deepcopy(self.next_state()))

    def compute_scale(self, size, field_size):
        self.multiplier = min((size.x - self.border_width * 2) / field_size.x,
                              (size.y - self.border_width * 2) / field_size.y)
        self.offset.x = (size.x - field_size.x * self.multiplier) / 2
        self.offset.y = (size.y - field_size.y * self.multiplier) / 2

    def fill(self,number):
        modulo=number%8
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

    def draw_image(self, state, size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x, size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.compute_scale(size, self.field)

        #constant part
        center_offset = self.offset_point(self.center)
        point_offset = self.offset_point(self.point)
        draw.circle((center_offset.x,center_offset.y),self.radius*self.multiplier,outline=self.fill(0))

        draw.circle((point_offset.x, point_offset.y), 1 * self.multiplier, fill="black")

        #iterating part

        for i in range(0,state):
            angle = i * 2* math.pi / 120
            new_center = self.center + Coords2D.turn(Coords2D(0,self.radius),angle)
            new_radius = (self.point- new_center).length() * self.multiplier
            new_center_offset = self.offset_point(new_center)
            draw.circle((new_center_offset.x, new_center_offset.y), new_radius, outline=self.fill(i+1))
        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img





