import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont

from moviepy import VideoFileClip, AudioFileClip
import music

class LongExpoCircle(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, points_no=10, min_power = 0, max_power = 200, delta_power = 0.02):
        super().__init__(size, length, rate, field_size, border)
        self.iter_no=0
        self.points_no=points_no
        self.curr_power = min_power
        self.max_power=max_power
        self.delta_power=delta_power

        self.radius = self.field.x*0.45
        self.center=Coords2D(self.field.x*0.5,self.field.y*0.5)


        self.file_name = "videos/ExpoCircle_Long" + str(self.max_power) + "_"

    def point(self, i):
        impact = i / self.points_no
        angle = impact * 2 * math.pi
        return self.center + Coords2D(math.cos(angle), math.sin(angle)) * self.radius

    def ext_point(self, i):
        impact = i / self.points_no
        angle = impact * 2 * math.pi
        return self.center + Coords2D(math.cos(angle), math.sin(angle)) * self.radius * 1.01

    def in_point(self, i):
        impact = i / self.points_no
        angle = impact * 2 * math.pi
        return self.center + Coords2D(math.cos(angle), math.sin(angle)) * self.radius * 0.99

    def next_state(self):
        self.iter_no+=1
        res =  {"iter_no":deepcopy(self.iter_no), "current_power":deepcopy(self.curr_power)}
        self.curr_power += self.delta_power
        return res

    def get_all_states(self):
        while (self.curr_power <= self.max_power):
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
            offset = self.offset_point(self.ext_point(i))
            offset_end = self.offset_point(self.in_point(i))
            draw.line((offset.x,offset.y,offset_end.x,offset_end.y), fill="black", width=1)
        #iterating part

        text_point = self.offset_point(Coords2D(10,10))
        font = ImageFont.truetype("segoesc.ttf", 20)


        draw.text((text_point.x, text_point.y),
                  "power = "+str(round(state["current_power"],3)), font=font, fill="black")

        for i in range(self.points_no):
            start = self.offset_point(self.point(i%self.points_no))
            end =  self.offset_point(self.point(int(math.pow(i,state["current_power"])) % self.points_no))
            draw.line([start.x,start.y,end.x,end.y],fill="black",width=2)

        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img

    def generate_video(self, sizes=None): #compress
        super().generate_video(sizes)
        video_clip = VideoFileClip(self.file_name + str(self.size.x) + '_' + str(self.size.y) + '.mp4')
        video_clip.write_videofile(self.file_name + "_final.mp4", codec="libx264", audio_codec="aac")

    def alternative_add_audio(self):
        sonic_vector = []
        notes_quantity=88
        for s in self.states:
            note_number = int(math.pow(s,self.power)) if self.power > 1 else s


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





