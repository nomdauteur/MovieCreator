import math
import os

import subprocess

from mingus.containers.note import Note
from mingus.containers.note_container import NoteContainer
from mingus.containers.bar import Bar
from mingus.containers.track import Track
import mingus.midi.midi_file_out as midi_file_out
from moviepy import VideoFileClip, AudioFileClip

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

    def offset_point(self,point):
        return Coords2D(self.offset.x,self.offset.y)+point*self.multiplier

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
        if (self.border_width==0):
            return
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
                        self.offset.x+self.field.x * self.multiplier+self.border_width, self.offset.y+self.field.y * self.multiplier+self.border_width),
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
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # Or 'XVID', 'DIVX', etc.
        self.get_all_states()
        for size in sizes:
            out = cv2.VideoWriter(self.file_name + str(size.x)+'_'+str(size.y)+'.mp4', fourcc, self.rate, (size.x, size.y))
            for cadre in self.states:

                img=self.draw_image(cadre,size)
                #img.show()
                #print("LOG: Plus image")
                frame_rgb = np.array(img)
                # Convert RGB to BGR (OpenCV's default color order)
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            cv2.destroyAllWindows()
            out.release()

    def get_note_container(self,state):
        return None

    def add_audio(self):
        b = Bar()
        t = Track()
        b.set_meter((self.rate,self.rate))
        bar_filling = 0
        print("I have {0} states: {1} seconds".format(len(self.states), len(self.states)/self.rate))
        for s in self.states:
            notes = self.get_note_container(s)
            b.place_notes(notes,self.rate)
            bar_filling+=1
            if (bar_filling == self.rate):
                print(len(b))
                t+b
                b = Bar()
                b.set_meter((self.rate, self.rate))
                bar_filling = 0
        t+b
        midi_file_out.write_Track("audio_assets/aaa.mid",t, bpm = 60*4)

        try:
            result = subprocess.run(
                ["fluidsynth", "-g", "3.0", "-F", "audio_assets/aaa.wav", "audio_assets/FluidR3_GM.sf2", "audio_assets/aaa.mid"],
                check=True, capture_output=True, text=True)
            print("Command ran successfully.")
            print("Output:\n", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Command failed with return code", e.returncode)
            print("Error output:\n", e.stderr)
        except FileNotFoundError:
            print("The command was not found. For Windows, try ['cmd', '/c', 'dir']")

        video_clip = VideoFileClip(self.file_name + str(self.size.x)+'_'+str(self.size.y)+'.mp4')


        audio_clip = AudioFileClip("audio_assets/aaa.wav")

        # Set the audio of the video clip to the new audio clip
        final_clip = video_clip.with_audio(audio_clip)

        # Write the final file (MoviePy handles the muxing internally using FFmpeg)

        final_clip.write_videofile(self.file_name+".mp4", codec="libx264", audio_codec="aac")





