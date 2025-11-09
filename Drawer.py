import random
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import string
from copy import deepcopy

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string


class Drawer:

    @staticmethod
    def num_to_color(num):
        return num

    def __init__(self, size=(1920,800),length=60,rate=1, field_size=(100,100),border=False):
        self.border_width=5 if border else 0
        self.offset_x = None
        self.offset_y = None
        self.multiplier = None
        self.border=border
        self.x,self.y=size
        self.field_x,self.field_y=field_size
        self.length = length
        self.rate = rate
        self.current_state=[[(0,0,0) for _ in range(self.field_x)] for _ in range(self.field_y)]
        self.time=0
        self.file_name="videos/"+generate_random_string(10)
        self.states=[]

    def next_state(self):
        self.time+=1
        for i in range(0,self.field_y):
            for j in range(0,self.field_x):
                self.current_state[i][j]=\
                    (random.randint(0,255),
                     random.randint(0,255),
                     random.randint(0,255))
        return self.current_state

    def get_all_states(self):
        for cadre in range(0, self.length*self.rate):
            self.states.append(deepcopy(self.next_state()))

    def draw_image(self,state,size=None):
        if size is None:
            size = (self.x, self.y)
        img = Image.new("RGB", size, (255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.multiplier = min((size[0]-self.border_width*2) / self.field_x, (size[1]-self.border_width*2) / self.field_y)
        self.offset_x = (size[0] - self.field_x * self.multiplier) / 2
        self.offset_y = (size[1] - self.field_y * self.multiplier) / 2
        for i in range(0, self.field_y):
            for j in range(0, self.field_x):
                draw.rectangle((self.offset_x+j*self.multiplier,self.offset_y+i*self.multiplier,
                                self.offset_x+(j+1)*self.multiplier,self.offset_y+(i+1)*self.multiplier),
                               self.num_to_color(state[i][j]))

        if (self.border):
            self.draw_border(draw)

        return img

    def draw_border(self,draw):
        color=(128,128,128)
        draw.rectangle((self.offset_x-self.border_width, self.offset_y-self.border_width,
                        self.offset_x, self.offset_y +self.field_y * self.multiplier+self.border_width),
                        color)
        draw.rectangle((self.offset_x -self.border_width, self.offset_y -self.border_width,
                        self.offset_x+self.field_x * self.multiplier+self.border_width, self.offset_y ),
                       color)
        draw.rectangle((self.offset_x  +self.field_x * self.multiplier, self.offset_y -self.border_width,
                        self.offset_x+self.field_x * self.multiplier+self.border_width, self.offset_y+self.field_y * self.multiplier+self.border_width),
                       color)
        draw.rectangle((self.offset_x -self.border_width, self.offset_y +self.field_y * self.multiplier,
                        self.offset_x+self.field_x * self.multiplier+self.border_width, self.offset_y+self.field_x * self.multiplier+self.border_width),
                       color)

    def generate_video(self, sizes=None):
        if sizes is None:
            sizes = [(self.x, self.y)]
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Or 'XVID', 'DIVX', etc.
        self.get_all_states()
        for size in sizes:
            out = cv2.VideoWriter(self.file_name + str(size[0])+'_'+str(size[1])+'.avi', fourcc, self.rate, (size[0], size[1]))
            for cadre in self.states:
                img=self.draw_image(cadre,size)
                print("LOG: Plus image")
                frame_rgb = np.array(img)
                # Convert RGB to BGR (OpenCV's default color order)
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            cv2.destroyAllWindows()
            out.release()



