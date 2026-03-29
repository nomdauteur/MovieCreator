import math

from Drawer import Drawer
from Coords2D import Coords2D

import random
from copy import deepcopy
from PIL import Image, ImageDraw, ImageFont
import music
from moviepy import VideoFileClip, AudioFileClip

class Methuselahs(Drawer):

    @staticmethod
    def num_to_color(num):
        no = num % (128*255*255)
        res = (math.floor(no/(255*255)),math.floor(no%(255*255)/255),math.floor(no%(255)))
        #print("Color {0} to {1}".format(no,res))
        return res

    def put_glider(self, point):
        if (point is None):
            point=Coords2D(self.field.x / 2, self.field.x / 2)
        x = point.x
        y = point.y
        self.initial_state[y][x]=1
        self.initial_state[y+2][x] = 1
        self.initial_state[y+1][x+1] = 1
        self.initial_state[y+2][x+1] = 1
        self.initial_state[y+1][x+2] = 1

    def put_toad(self, point):
        if (point is None):
            point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = point.x
        y = point.y
        self.initial_state[y][x]=1
        self.initial_state[y][x+1] = 1
        self.initial_state[y][x+2] = 1
        self.initial_state[y+1][x-1] = 1
        self.initial_state[y+1][x] = 1
        self.initial_state[y + 1][x + 1] = 1

    def put_line(self, point):
        dir = random.randint(0,1)
        if (point is None):
            point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = point.x
        y = point.y
        self.initial_state[y][x] = 1
        self.initial_state[y+dir][x+(1-dir)] = 1
        self.initial_state[y+2*dir][x+2*(1-dir)] = 1

    def put_long_line(self):
        dir = random.randint(0,1)
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)
        y = math.floor(point.y)
        self.initial_state[y][x] = 1
        self.initial_state[y+dir][x+(1-dir)] = 1
        self.initial_state[y+2*dir][x+2*(1-dir)] = 1
        self.initial_state[y + 3 * dir][x + 3 * (1 - dir)] = 1

    def put_tetris(self):
        dir = random.randint(0,1)
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)
        y = math.floor(point.y)
        self.initial_state[y][x] = 1
        self.initial_state[y][x+1] = 1
        self.initial_state[y][x+2] = 1
        self.initial_state[y -1][x + 1] = 1

    def put_block(self, point):
        if (point is None):
            point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = point.x
        y = point.y
        self.initial_state[y][x] = 1
        self.initial_state[y][x+1] = 1
        self.initial_state[y+1][x] = 1
        self.initial_state[y+1][x+1] = 1

    def put_r_pentamino(self):
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)
        y = math.floor(point.y)
        self.initial_state[y][x+1] = 1
        self.initial_state[y][x+2] = 1
        self.initial_state[y+1][x] = 1
        self.initial_state[y+1][x+1] = 1
        self.initial_state[y + 2][x + 1] = 1

    def put_rabbit(self):
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)
        y = math.floor(point.y)
        self.initial_state[y][x] = 1
        self.initial_state[y][x+4] = 1
        self.initial_state[y][x + 5] = 1
        self.initial_state[y][x + 6] = 1
        self.initial_state[y+1][x] = 1
        self.initial_state[y+1][x+1] = 1
        self.initial_state[y + 1][x + 2] = 1
        self.initial_state[y + 1][x + 5] = 1
        self.initial_state[y + 2][x + 1] = 1

    def put_acorn(self):
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)
        y = math.floor(point.y)

        self.initial_state[y][x+1] = 1
        self.initial_state[y+1][x+3] = 1
        self.initial_state[y+2][x] = 1
        self.initial_state[y+2][x+1] = 1
        self.initial_state[y+2][x+4] = 1
        self.initial_state[y+2][x+5] = 1
        self.initial_state[y+2][x+6] = 1

    def block_plus_line(self):
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)
        y = math.floor(point.y)

        self.initial_state[y][x] = 1
        self.initial_state[y][x + 1] = 1
        self.initial_state[y + 1][x] = 1
        self.initial_state[y + 1][x + 1] = 1

        self.initial_state[y+1][x+3] = 1
        self.initial_state[y + 1][x + 4] = 1
        self.initial_state[y + 1][x + 5] = 1

    def herschel(self):
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)
        y = math.floor(point.y)

        self.initial_state[y][x] = 1
        self.initial_state[y+1][x] = 1
        self.initial_state[y + 1][x+1] = 1
        self.initial_state[y + 1][x + 2] = 1

        self.initial_state[y+2][x] = 1
        self.initial_state[y + 2][x + 2] = 1
        self.initial_state[y + 3][x + 2] = 1

    def onedglidergen(self):
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)-7
        y = math.floor(point.y)

        self.initial_state[y][x] = 1
        self.initial_state[y][x+1] = 1
        self.initial_state[y][x+2] = 1
        self.initial_state[y][x + 3] = 1
        self.initial_state[y][x + 6] = 1
        self.initial_state[y][x + 7] = 1
        self.initial_state[y][x + 8] = 1
        self.initial_state[y][x + 10] = 1
        self.initial_state[y][x + 11] = 1
        self.initial_state[y][x + 12] = 1
        self.initial_state[y][x + 13] = 1
        self.initial_state[y][x + 14] = 1

    def onedten(self):
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)-7
        y = math.floor(point.y)

        self.initial_state[y][x] = 1
        self.initial_state[y][x+1] = 1
        self.initial_state[y][x+2] = 1
        self.initial_state[y][x + 3] = 1
        self.initial_state[y][x + 4] = 1
        self.initial_state[y][x + 5] = 1
        self.initial_state[y][x + 6] = 1
        self.initial_state[y][x + 7] = 1
        self.initial_state[y][x + 8] = 1
        self.initial_state[y][x + 9] = 1


    def one56(self):
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)-28
        y = math.floor(point.y)
        for i in range(56):
            self.initial_state[y][x+i] = 1

    def twotetris(self):
        point = Coords2D(self.field.x / 2, self.field.x / 2)
        x = math.floor(point.x)-5
        y = math.floor(point.y)
        self.initial_state[y][x+1] = 1
        self.initial_state[y+1][x] = 1
        self.initial_state[y+1][x + 1] = 1
        self.initial_state[y+1][x+2] = 1

        self.initial_state[y][x + 7] = 1
        self.initial_state[y + 1][x+6] = 1
        self.initial_state[y + 1][x + 7] = 1
        self.initial_state[y + 1][x + 8] = 1



    def init(self):
        self.twotetris()

    def __init__(self, size=Coords2D(1080, 1920), length=60, rate=30, field_size=Coords2D(100, 100), border=False, births=[3], stables=[2,3], initial_state=None):
        super().__init__(size, length, rate, field_size,border)
        self.draw_time = 0
        self.births=births
        self.stables=stables
        self.initial_state = [[0 for _ in range(self.field.x)] for _ in range(self.field.y)]

        self.init()

        self.current_state=deepcopy(self.initial_state)

    def count_neighbors(self, i, j, state):
        res = 0
        for a in range(-1,2):
            for b in range(-1,2):
                if (a == 0 and b == 0) :
                    continue
                if (i + a < 0 or i + a >= self.field.y or j + b < 0 or j + b >= self.field.x):
                    continue
                res += state[i+a][j+b]
        return res

    def next_state(self):
        print("State no: {0}".format(self.time))
        self.time+=1
        tmp_state = deepcopy(self.current_state)
        for i in range(0, self.field.y):
            for j in range(0, self.field.x):
                n = self.count_neighbors(i, j, tmp_state)
                if (n in self.births):
                    self.current_state[i][j] = 1
                elif (n in self.stables):
                    continue
                else:
                    self.current_state[i][j] = 0

        return self.current_state

    def draw_image(self,state,size=None):
        self.draw_time += 1
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.compute_scale(size)
        for i in range(0, self.field.y):
            for j in range(0, self.field.x):
                begin = self.offset_point(Coords2D(j, i))
                end = self.offset_point(Coords2D(j + 1, i + 1))
                draw.rectangle((begin.x,begin.y,end.x,end.y),
                               self.num_to_color(math.floor(self.draw_time)) if state[i][j]==1 else (255,255,255))

        if (self.border):
            self.draw_border(draw)
        self.watermark(draw)

        return img


    def alternative_add_audio(self):
        scale = [
    261.63,  # C4
    329.63,  # E4
    392.00,  # G4
    493.88   # B4
]
        sonic_vector = []
        notes_quantity=88
        i=0
        for s in self.states:
            note_number = scale[i%len(scale)]
            i+=1

            sound = music.core.synths.note(freq=note_number,
                                           duration=1.0/self.rate)
            sonic_vector.append(sound)
        stack = music.utils.horizontal_stack(*sonic_vector)

        music.core.io.write_wav_mono(sonic_vector=stack,
                                     filename='audio_assets/aaa.wav')

        video_clip = VideoFileClip(self.file_name + str(self.size.x)+'_'+str(self.size.y)+'.mp4')


        audio_clip = AudioFileClip("audio_assets/aaa.wav")

        # Set the audio of the video clip to the new audio clip
        final_clip = video_clip.with_audio(audio_clip)

        # Write the final file (MoviePy handles the muxing internally using FFmpeg)

        final_clip.write_videofile(self.file_name+".mp4", codec="libx264", audio_codec="aac")