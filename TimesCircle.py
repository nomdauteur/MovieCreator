import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont

class TimesCircle(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, points_no=10, factor = 2, iters = 40):
        super().__init__(size, length, rate, field_size, border)
        self.iter_no=0
        self.points_no=points_no
        self.factor=factor
        self.iters=iters

        self.radius = self.field.x*0.45
        self.center=Coords2D(self.field.x*0.5,self.field.y*0.5)

        self.points = Coords2D.make_regular_polygon(self.points_no,self.center,self.radius)
        self.text_points = Coords2D.make_regular_polygon(self.points_no,self.center,self.radius*1.05)

        self.file_name = "videos/TimesCircle_" + str(self.factor)+"_"

    def next_state(self):
        self.iter_no+=1
        return deepcopy(self.iter_no)

    def get_all_states(self):
        for i in range(self.iters):
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

        ellipse_start = self.offset_point(self.center+Coords2D(-self.radius,-self.radius))
        ellipse_end = self.offset_point(self.center+Coords2D(self.radius,self.radius))

        draw.ellipse([(ellipse_start.x,ellipse_start.y),ellipse_end.x,ellipse_end.y],
                     fill="white",outline="black", width=4)
        for i in range(self.points_no):
            offset = self.offset_point(self.points[i])
            offset_end = self.offset_point(self.points[i]+Coords2D(1,1))
            #draw.rectangle((offset.x,offset.y,offset_end.x,offset_end.y), fill="red")
            font = ImageFont.truetype("arial.ttf", 7)
            text_point = self.offset_point(self.text_points[i])
            draw.text((text_point.x, text_point.y),
                      str(i), font=font, fill="black")
        #iterating part
        for i in range(1,state+1):
            start = self.offset_point(self.points[(i%self.points_no)])
            end =  self.offset_point(self.points[(self.factor*i)%self.points_no])
            draw.line([start.x,start.y,end.x,end.y],fill=self.fill(i),width=2)

        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img





