import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont


class Julia(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,
                 degree=2,c=Coords2D(0,0)):
        super().__init__(size, length, rate, field_size, border)
        self.degree = degree
        self.c = c
        self.z_c = [[self.coords_to_z(Coords2D(j,i)) for j in range(self.field.x)] for i in range(self.field.y)]
        self.file_name = "videos/"+"Julia_"+str(self.c.x)+"_"+str(self.c.y)+"_"+str(self.degree)+"_"

    def z_to_coords(self, z):
        return (z + Coords2D(self.field.x/2, self.field.y/2)) * 100

    def coords_to_z(self,coords):
        return (coords - Coords2D(self.field.x / 2, self.field.y / 2)) /100.0

    def next_z_c(self,z_c):
        if (abs(z_c.x) > 2**16 ): # if it's big, it's big
            return Coords2D(2**16,z_c.y)
        if (abs(z_c.y) > 2**16): # if it's big, it's big
            return Coords2D(z_c.x,2**16)
        return z_c.complex_pow(self.degree)+self.c

    def fill(self,number):
        match number:
            case 7:
                return 'red'
            case 6:
                return 'green'
            case 5:
                return 'blue'
            case 4:
                return 'yellow'
            case 3:
                return 'purple'
            case 2:
                return 'pink'
            case 1:
                return 'gray'
            case 0:
                return 'black'
            case _:
                return 'white'




    def next_state(self):
        print("Plus state")

        self.z_c = [[self.next_z_c(self.z_c[i][j]) for j in range(self.field.x)] for i in range(self.field.y)]

        return deepcopy(self.z_c)


    def get_all_states(self):
        self.states=[deepcopy(self.z_c)]

        for i in range(30):
            self.states.append(deepcopy(self.next_state()))

    def draw_image(self, state, size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x, size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.compute_scale(size)
        #print(state)

        for i in range(self.field.x):
            for j in range(self.field.y):
                begin = self.offset_point(Coords2D(j,i))
                end = self.offset_point(Coords2D(j+1, i+1))
                color = 0 if state[i][j].length()<2 else 1 if state[i][j].length()<2**3 else 2 \
                    if state[i][j].length()<2**5 else 3 if state[i][j].length()<2**7 else 4 \
                    if state[i][j].length() < 2**9 else 5 if state[i][j].length()<2**11 else 6 \
                    if state[i][j].length() < 2**13 else 7 if state[i][j].length()<2**15 else 8
                #print("Value is {0}, color is {1}".format(state[i][j],self.fill(color)))
                draw.rectangle((begin.x,begin.y,end.x,end.y),fill=self.fill(color))



        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img


