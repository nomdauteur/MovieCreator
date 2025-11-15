import random
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import string
from copy import deepcopy
from datetime import datetime

from Coords2D import Coords2D

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string


class Drawer:

    @staticmethod
    def num_to_color(num):
        return num

    def __init__(self, size=Coords2D(1920,800),length=60,rate=1, field_size=Coords2D(100,100),border=False):
        self.border_width=5 if border else 0
        self.offset=Coords2D(None,None)
        self.multiplier = None
        self.border=border
        self.size=size
        self.field=field_size
        self.length = length
        self.rate = rate
        self.current_state=[[(0,0,0) for _ in range(self.field.x)] for _ in range(self.field.y)]
        self.time=0
        self.file_name="videos/"+__class__.__name__+"_"+datetime.now().strftime("%Y%m%dT%H%M%S")+"_"+generate_random_string(10)
        self.states=[]

    def next_state(self):
        self.time+=1
        for i in range(0,self.field.y):
            for j in range(0,self.field.x):
                self.current_state[i][j]=\
                    (random.randint(0,255),
                     random.randint(0,255),
                     random.randint(0,255))
        return self.current_state

    def get_all_states(self):
        for cadre in range(0, self.length*self.rate):
            self.states.append(deepcopy(self.next_state()))

    def compute_scale(self, size):
        self.multiplier = min((size.x - self.border_width * 2) / self.field.x,
                              (size.y - self.border_width * 2) / self.field.y)
        self.offset.x = (size.x - self.field.x * self.multiplier) / 2
        self.offset.y = (size.y - self.field.y * self.multiplier) / 2

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.compute_scale(size)
        for i in range(0, self.field.y):
            for j in range(0, self.field.x):
                draw.rectangle((self.offset.x+j*self.multiplier,self.offset.y+i*self.multiplier,
                                self.offset.x+(j+1)*self.multiplier,self.offset.y+(i+1)*self.multiplier),
                               self.num_to_color(state[i][j]))

        if (self.border):
            self.draw_border(draw)
        self.watermark(draw)

        return img

    def draw_border(self,draw):
        color=(128,128,128)
        draw.rectangle((self.offset.x-self.border_width, self.offset.y-self.border_width,
                        self.offset.x, self.offset.y +self.field.y * self.multiplier+self.border_width),
                        color)
        draw.rectangle((self.offset.x -self.border_width, self.offset.y -self.border_width,
                        self.offset.x+self.field.x * self.multiplier+self.border_width, self.offset.y ),
                       color)
        draw.rectangle((self.offset.x  +self.field.x * self.multiplier, self.offset.y -self.border_width,
                        self.offset.x+self.field.x * self.multiplier+self.border_width, self.offset.y+self.field.y * self.multiplier+self.border_width),
                       color)
        draw.rectangle((self.offset.x -self.border_width, self.offset.y +self.field.y * self.multiplier,
                        self.offset.x+self.field.x * self.multiplier+self.border_width, self.offset.y+self.field.x * self.multiplier+self.border_width),
                       color)

    def watermark(self,draw):
        if (self.offset.x>self.offset.y):
            x=self.offset.x+self.field.x*self.multiplier+2*self.border_width+2
            y=self.offset.y+self.field.y*self.multiplier
        else:
            x=self.offset.x+self.field.x*self.multiplier/2
            y=self.offset.y+self.field.y*self.multiplier+2*self.border_width+2
        font = ImageFont.truetype("arial.ttf", 15)
        draw.text((x,y),"@matphysdat", font=font, fill="black")


    def generate_video(self, sizes=None):
        if sizes is None:
            sizes = [self.size]
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Or 'XVID', 'DIVX', etc.
        self.get_all_states()
        for size in sizes:
            out = cv2.VideoWriter(self.file_name + str(size.x)+'_'+str(size.y)+'.avi', fourcc, self.rate, (size.x, size.y))
            for cadre in self.states:

                img=self.draw_image(cadre,size)
                #print("LOG: Plus image")
                frame_rgb = np.array(img)
                # Convert RGB to BGR (OpenCV's default color order)
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            cv2.destroyAllWindows()
            out.release()



