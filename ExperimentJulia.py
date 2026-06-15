import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont


class ExperimentJulia(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,
                 degree=2,c=Coords2D(0,0)):
        super().__init__(size, length, rate, field_size, border)
        self.degree = degree
        self.c = c
        self.z_c = [[self.coords_to_z(Coords2D(j,i)) for j in range(self.field.x)] for i in range(self.field.y)]
        self.file_name = "videos/"+"ZnCompCosZ1Julia_"+str(self.c.x)+"_"+str(self.c.y)+"_"+str(self.degree)+"_"

    def z_to_coords(self, z):
        return (z + Coords2D(self.field.x/2, self.field.y/2)) * self.field.x/6

    def coords_to_z(self,coords):
        return (coords - Coords2D(self.field.x / 2, self.field.y / 2)) /self.field.x*6

    def next_z_c(self,z_c):
        if (abs(z_c.x) > 2**8 ): # if it's big, it's big
            return Coords2D(2**8,z_c.y)
        if (abs(z_c.y) > 2**8): # if it's big, it's big
            return Coords2D(z_c.x,2**8)
        #to_pow = Coords2D(z_c.y, z_c.x)
        #return to_pow.complex_pow(self.degree)+self.c
        #return z_c.complex_pow(self.degree) * math.cos(z_c.length() * 4 * math.pi) + self.c
        #return z_c.complex_pow(self.degree) * math.sin(z_c.x * 4 * math.pi) * math.cos(z_c.y * 4 * math.pi) + self.c
        #pow = z_c.complex_pow(self.degree)
        #return Coords2D(abs(pow.x), pow.y) + self.c
        try:
            #return z_c.complex_pow(self.degree).complex_cos()+self.c
            return z_c.complex_pow(self.degree).complex_mul(z_c.complex_cos()) + self.c
        except OverflowError:
            return z_c

    def fill(self,number):
        match number:
            case 8:
                return 'orange'
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

        for i in range(12):
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
                color = 0 if state[i][j].length()<0.5 else 1 if state[i][j].length()<1 else 2 \
                    if state[i][j].length()<2 else 3 if state[i][j].length()<4 else 4 \
                    if state[i][j].length() < 8 else 5 if state[i][j].length()<16 else 6 \
                    if state[i][j].length() < 32 else 7 if state[i][j].length()<64 else 8 \
                    if state[i][j].length() < 128 else 9

                #print("Value is {0}, color is {1}".format(state[i][j],self.fill(color)))
                draw.rectangle((begin.x,begin.y,end.x,end.y),fill=self.fill(color))



        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img


