from Drawer import Drawer
from Coords2D import Coords2D

import random
from copy import deepcopy
import math
from moviepy import VideoFileClip, AudioFileClip
import music
from PIL import Image, ImageDraw, ImageFont

class RandomWalk(Drawer):
    colors = [(255,255,255) if i == 0 else (random.randint(0,255),random.randint(0,255),random.randint(0,255)) for i in range(80)]

    @staticmethod
    def num_to_color(num):

        return RandomWalk.colors[num % len(RandomWalk.colors)]


    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100),
                 border=False, walkers_count=5):
        super().__init__(size, length, rate, field_size,border)
        self.walkers_count = walkers_count


        self.current_points = [Coords2D(random.randint(0,self.field.x-1),random.randint(0,self.field.y-1)) for i in range(self.walkers_count)]
        self.initial_points = deepcopy(self.current_points)
        self.sound = [set([self.initial_points[i].x*self.field.y+self.field.y for i in range(self.walkers_count)])]
        self.has_returned=[0 for i in range(self.walkers_count)]
        self.court=[[0 for _ in range(self.field.x)] for _ in range(self.field.y)]
        for i in range(len(self.current_points)):
            self.court[self.current_points[i].y][self.current_points[i].x]=i+1
        self.current_state={"field":deepcopy(self.court),"points":deepcopy(self.current_points)}
        self.should_continue=True


    def is_available(self, coords : Coords2D):
        return (0 <= coords.x < self.field.x) \
            and (0 <= coords.y < self.field.y) and \
            coords not in self.current_points

    def near_neighbors(self, coords : Coords2D):
        return [i for i in
                [Coords2D(coords.x,coords.y-1),Coords2D(coords.x,coords.y+1),
                 Coords2D(coords.x-1,coords.y),Coords2D(coords.x+1,coords.y)] if self.is_available(i) ]

    def next_state(self):
        sound=[]
        self.time+=1

        for i in range(len(self.current_points)):
            if self.has_returned[i]==1:
                continue
            neighbors=self.near_neighbors(self.current_points[i])
            if len(neighbors)==0:
                continue
            self.current_points[i] = random.choice(neighbors)
            self.court[self.current_points[i].y][self.current_points[i].x]=i+1
            sound.append(self.current_points[i].x*self.field.y+self.field.y)
            if self.current_points[i]==self.initial_points[i]:
                self.has_returned[i]=1

        self.sound.append(set(sound))
        return {"field":deepcopy(self.court),"points":deepcopy(self.current_points)}


    def get_all_states(self):
        self.states = [deepcopy(self.current_state)]
        cnt=0
        #while(sum(self.has_returned)<self.walkers_count and cnt <self.rate*self.length):
        while (sum(self.has_returned) < self.walkers_count):
            self.states.append(deepcopy(self.next_state()))
            cnt+=1
            if (cnt%10==0):
                print("{0}th cadre".format(cnt))
                print("{0} returned".format(sum(self.has_returned)))

    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.compute_scale(size)
        for i in range(0, self.field.y):
            for j in range(0, self.field.x):
                begin = self.offset_point(Coords2D(j,i))
                end = self.offset_point(Coords2D(j+1,i+1))
                draw.rectangle((begin.x, begin.y, end.x, end.y),
                               self.num_to_color(state["field"][i][j]), outline=(128,128,128),width=5 if Coords2D(j,i) in state["points"] or Coords2D(j,i) in self.initial_points else 0)

        if (self.border):
            self.draw_border(draw)
        self.watermark(draw)

        return img


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
        print("Cadre length: {0}, sound length: {1}".format(len(self.states), len(self.sound)))
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