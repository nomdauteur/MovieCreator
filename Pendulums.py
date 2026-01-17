import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont

from moviepy import VideoFileClip, AudioFileClip
import music

class Pendulums(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,points_no=3, stick_lengths = [10,20],rules=[0,1,2], accelerated = False):
        # rules will be mapped to functions. E. g. 0 not moving, 1 circle etc.
        super().__init__(size, length, rate, field_size, border)
        self.points_no=points_no
        self.stick_lengths=stick_lengths
        self.rules=rules
        self.initial_point = Coords2D(self.field.x/2,self.field.y/2)
        self.phis=[0 for i in range(0,self.points_no)] # will play with that too; 0 should be downward
        self.delta_phi = 2*math.pi/360
        self.init_positions=[]
        self.init_positions.append(self.initial_point)
        for i in range(1,self.points_no):
            self.init_positions.append(self.init_positions[i-1]+Coords2D(math.cos(self.phis[i] - math.pi/2),math.sin(self.phis[i] - math.pi/2))*self.stick_lengths[i-1])
        self.lines = [[(self.init_positions[i],self.init_positions[i+1])] for i in range(0,self.points_no-1)]
        self.accelerated = accelerated

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


    def map_to_function(self,point_no, parameter):
        index = self.rules[point_no]
        length_addon=Coords2D(0, 0) if point_no==0 else Coords2D(0,-self.stick_lengths[point_no-1])
        if (index < 0):
            return Coords2D(math.sin(self.phis[point_no]*abs(index))*self.field.x/10,0)+length_addon
        if (index == 0):
                return length_addon
        else:
            return Coords2D(math.cos(index * parameter- math.pi/2),math.sin(index * parameter- math.pi/2)) * self.stick_lengths[point_no-1]

    def get_positions(self):
        acceleration = 0 if not self.accelerated else 0.1
        result = [self.initial_point+self.map_to_function(0, self.phis[0])]
        for i in range(1,self.points_no):
            result.append(result[i-1]+self.map_to_function(i, self.phis[i])+Coords2D(0,acceleration)*self.phis[0]*self.phis[0])
        return result

    def step(self):
        self.phis=[a+self.delta_phi for a in self.phis]

    def next_state(self):
        self.step()
        positions = self.get_positions()
        for i in range(0, self.points_no - 1):
            self.lines[i].append((positions[i],positions[i+1]) )
        return len(self.lines[0])


    def get_all_states(self):
        self.states=[self.points_no-1]

        for i in range(360):
            self.states.append(deepcopy(self.next_state()))

    def draw_image(self, state, size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x, size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.compute_scale(size)

        for i in range(state):
            for j in range(self.points_no-1):
                start = self.offset_point(self.lines[j][i][0])
                end =  self.offset_point(self.lines[j][i][1])
                draw.line([start.x,start.y,end.x,end.y],fill=self.fill(j),width=2)
                draw.circle((start.x,start.y),self.multiplier,fill="white",outline="black",width=1)
                draw.circle((end.x, end.y),self.multiplier, fill="white", outline="black", width=1)


        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img


