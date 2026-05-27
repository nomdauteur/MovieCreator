from Drawer import Drawer
from Coords2D import Coords2D

import random
from copy import deepcopy
import math
from moviepy import VideoFileClip, AudioFileClip
import music

class MultiGameOfLife(Drawer):
    colors = [(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)) for i in range(20)]

    @staticmethod
    def num_to_color(num):

        return MultiGameOfLife.colors[num % len(MultiGameOfLife.colors)]

    def onedten(self, color):
        point = Coords2D(random.randint(10,self.field.x -10), random.randint(10,self.field.x -10))
        dir = random.randint(0,1)
        x = math.floor(point.x)-7
        y = math.floor(point.y)

        self.initial_state[y][x] = color
        self.initial_state[y+1*dir][x+1*(1-dir)] = color
        self.initial_state[y+2*dir][x+2*(1-dir)] = color
        self.initial_state[y+3*dir][x + 3*(1-dir)] = color
        self.initial_state[y+4*dir][x + 4*(1-dir)] = color
        self.initial_state[y+5*dir][x + 5*(1-dir)] = color
        self.initial_state[y+6*dir][x + 6*(1-dir)] = color
        self.initial_state[y+7*dir][x + 7*(1-dir)] = color
        self.initial_state[y+8*dir][x + 8*(1-dir)] = color
        self.initial_state[y+9*dir][x + 9*(1-dir)] = color


    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100),
                 border=False, agents=[{"births":[3],"stable":[2,3]}, {"births":[3],"stable":[2,3]}, {"births":[3],"stable":[2,3]}], initial_state=None):
        super().__init__(size, length, rate, field_size,border)
        self.agents = agents





        self.initial_state = deepcopy(initial_state)

        self.sound=[]

        if initial_state is None:
            initial_state = [[0 for _ in range(self.field.x)] for _ in range(self.field.y)]
            self.initial_state=deepcopy(initial_state)
            for i in range(0, len(self.agents)):
                #self.onedten(i+1)
                off = random.randint(3,15)
                rand_x=random.randint(0,self.field.y-off-1)
                rand_y=random.randint(0,self.field.x-off-1)
                for a in range(0,off):
                    for b in range(0, off):
                        self.initial_state[rand_x + a][rand_y +b] = (i + 1) * random.randint(0,1)


        self.current_state=deepcopy(self.initial_state)
        self.should_continue=True

    def count_neighbors(self, i, j, state, color):
        res = 0
        for a in range(-1,2):
            for b in range(-1,2):
                if (a == 0 and b == 0) :
                    continue
                if (i + a < 0 or i + a >= self.field.y or j + b < 0 or j + b >= self.field.x):
                    continue
                if (state[i+a][j+b] == color):
                    res += 1
        return res

    def next_state(self):
        sound=[]
        self.time+=1
        self.should_continue=False

        for c in range(1, len(self.agents) + 1):
            tmp_state = deepcopy(self.current_state)
            for i in range(0, self.field.y):
                for j in range(0, self.field.x):
                    if (tmp_state[i][j]!=0 and tmp_state[i][j]!=c):
                        #print("A{0}.{1}".format(i,j))
                        continue
                    n = self.count_neighbors(i, j, tmp_state, c)
                    if (tmp_state[i][j]==0 and n in self.agents[c-1]["births"]):
                        self.should_continue=True
                        sound.append(c)
                        #print("birthing {0}".format(self.num_to_color(c)))
                        self.current_state[i][j] = c
                    elif (n in self.agents[c-1]["stable"]):
                        continue
                    else:

                        self.current_state[i][j] = 0

        self.sound.append(set(sound))
        return self.current_state


    def get_all_states(self):
        self.states = [deepcopy(self.current_state)]
        cnt=0
        while(self.should_continue and cnt <self.rate*10):
            self.states.append(deepcopy(self.next_state()))
            cnt+=1
            if (cnt%10==0):
                print("{0}th cadre".format(cnt))

    def alternative_add_audio(self):
        sonic_vector = []
        map = [
            261.63,  # C4
            293.66,  # D4
            329.63,  # E4
            349.23,  # F4
            392.00,  # G4
            440.00,  # A4
            493.88  # B4
        ]
        notes_quantity=88
        for s in self.sound:

            note_numbers = [map[i%len(map)] for i in s]

            sound = [music.core.synths.note(freq=note_number,
                                           duration=1.0/self.rate) for note_number in note_numbers]
            if len(sound)!=0:
                sonic_vector.append(random.choice(sound))
            else:
                sonic_vector.append(music.core.synths.note(freq=0,
                                           duration=1.0/self.rate))

        stack = music.utils.horizontal_stack(*sonic_vector)

        music.core.io.write_wav_mono(sonic_vector=stack,
                                     filename='audio_assets/aaa.wav')

        video_clip = VideoFileClip(self.file_name + str(self.size.x)+'_'+str(self.size.y)+'.mp4')


        audio_clip = AudioFileClip("audio_assets/aaa.wav")

        # Set the audio of the video clip to the new audio clip
        final_clip = video_clip.with_audio(audio_clip)

        # Write the final file (MoviePy handles the muxing internally using FFmpeg)

        final_clip.write_videofile(self.file_name+".mp4", codec="libx264", audio_codec="aac")