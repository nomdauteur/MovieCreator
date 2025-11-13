import random

from Drawer import Drawer
from Coords2D import Coords2D
import cv2
from PIL import Image, ImageDraw, ImageFont


class PolyLineDrawer(Drawer):

    @staticmethod
    def num_to_color(num):
        return (255, 255, 255) if num == 1 else (0, 0, 0)

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False):
        super().__init__(size, length, rate, field_size, border)
        self.poly_lines=[]
        self.poly_lines.append(Coords2D(random.randint(0,self.field.x),random.randint(0,self.field.y)))
        self.direction=None
        self.matrix=[[0 for _ in range(self.field.x)] for _ in range(self.field.y)]

    def next_state(self):
        self.time+=1
        print("LOG: current dir: {0}".format(self.direction))

        #find next available place
        available_dirs=[]
        current_point = self.poly_lines[-1]
        turnable_flag = False
        stayable_flag = False

        if (self.direction==None):
            turnable_flag = True
            stayable_flag = True
            for dir in [Coords2D(1,0),Coords2D(0,1),Coords2D(-1,0),Coords2D(0,-1)]:
                possible_point=current_point+dir
                if (0<=possible_point.x<self.field.x) and (0<=possible_point.y<self.field.y):
                    available_dirs.append(dir)
            self.direction=available_dirs[0]


        else:
            stay_point=current_point+self.direction
            turn_dirs=[Coords2D(0,0)-self.direction,Coords2D(self.direction.y,self.direction.x),Coords2D(-self.direction.y,-self.direction.x)]
            if 0<=stay_point.x<self.field.x and 0<=stay_point.y<self.field.y:
                stayable_flag=(self.matrix[stay_point.y][stay_point.x]==0)
            else:
                stayable_flag=False

            for turn_dir in turn_dirs:
                turn_point=current_point+turn_dir
                if (0 <= turn_point.x < self.field.x and 0 <= turn_point.y < self.field.y):
                    if (self.matrix[turn_point.y][turn_point.x] == 0):
                        turnable_flag=True
                        available_dirs.append(turn_dir)
        #draw
        if (not stayable_flag and not turnable_flag):
            #print("No effing way to go")
            return self.poly_lines

        if (not stayable_flag and turnable_flag):
            self.direction=random.choice(available_dirs)

        if (stayable_flag and turnable_flag):
            want_to_turn = random.randint(0,1)
            if (want_to_turn):
                self.direction=random.choice(available_dirs)

        self.poly_lines.append(current_point + self.direction)
        self.matrix[self.poly_lines[-1].y][self.poly_lines[-1].x] = 1

        print("LOG: available dirs:")
        for a in available_dirs:
            print(a)
        print("LOG: chosen dir: {0}".format(self.direction))

        return self.poly_lines


    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.multiplier = min((size.x-self.border_width*2) / self.field.x, (size.y-self.border_width*2) / self.field.y)
        self.offset.x = (size.x - self.field.x * self.multiplier) / 2
        self.offset.y = (size.y - self.field.y * self.multiplier) / 2
        for i in range(0, len(state)-1):
            #print("DRAWING: {0} to {1}".format(state[i],state[i+1]))
            draw.line([self.offset.x+state[i].x*self.multiplier,
                       self.offset.y+state[i].y*self.multiplier,
                       self.offset.x + state[i+1].x*self.multiplier,
                       self.offset.y+state[i+1].y*self.multiplier], fill="black", width=5)

        if (self.border):
            self.draw_border(draw)
        self.grid(draw)
        self.watermark(draw)

        return img

    def grid(self,draw):
        for i in range(self.field.y):
            draw.line([self.offset.x,
                           self.offset.y+i * self.multiplier,
                           self.offset.x + self.field.x * self.multiplier,
                           self.offset.y+i*self.multiplier], fill="lightcyan", width=2)

        for i in range(self.field.x):
            draw.line([self.offset.x +i * self.multiplier,
                       self.offset.y,
                           self.offset.x + i * self.multiplier,
                           self.offset.y+self.field.y*self.multiplier], fill="lightcyan", width=2)

