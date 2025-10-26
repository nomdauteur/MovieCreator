import random
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

class Drawer:
    def __init__(self, size=(1920,800),length=60,rate=1, field_size=(100,100)):
        self.x,self.y=size
        self.field_x,self.field_y=field_size
        self.length = length
        self.rate = rate
        self.current_state=[[(0,0,0) for _ in range(self.field_x)] for _ in range(self.field_y)]
        self.time=0
        self.file_name=generate_random_string(10)
        self.multiplier=min(self.x/self.field_x,self.y/self.field_y)
        self.offset_x=(self.x-self.field_x*self.multiplier)/2
        self.offset_y = (self.y - self.field_y * self.multiplier) / 2

    def next_state(self):
        self.time+=1
        for i in range(0,self.field_y):
            for j in range(0,self.field_x):
                self.current_state[i][j]=\
                    (random.randint(0,255),
                     random.randint(0,255),
                     random.randint(0,255))

    def draw_image(self):
        img = Image.new("RGB", (self.x, self.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        for i in range(0, self.field_y):
            for j in range(0, self.field_x):
                draw.rectangle((self.offset_x+j*self.multiplier,self.offset_y+i*self.multiplier,
                                self.offset_x+(j+1)*self.multiplier,self.offset_y+(i+1)*self.multiplier),
                               self.current_state[i][j])

        return img

    def generate_video(self):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Or 'XVID', 'DIVX', etc.
        out = cv2.VideoWriter(self.file_name+'.avi', fourcc, self.rate, (self.x, self.y))
        for cadre in range(0, self.length*self.rate):
            self.next_state()
            img=self.draw_image()
            print("LOG: Working on {0}th image".format(cadre))
            frame_rgb = np.array(img)
            # Convert RGB to BGR (OpenCV's default color order)
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            out.write(frame_bgr)
        cv2.destroyAllWindows()
        out.release()



