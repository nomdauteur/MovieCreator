import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont


class ExperimentMandelbrot(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,
                 degree=2,start=Coords2D(0,0)):
        super().__init__(size, length, rate, field_size, border)
        self.degree = degree
        self.start = start
        self.z_c = [[self.start for _ in range(self.field.x)] for _ in range(self.field.y)]
        self.file_name="videos/ZnTimesCompCosZnMandelbrot_"+str(self.degree)+"_"

    def c_to_coords(self, c):
        return (c + Coords2D(self.field.x/2, self.field.y/2)) * 100

    def coords_to_c(self,coords):
        return (coords - Coords2D(self.field.x / 2, self.field.y / 2)) /100.0

    def next_z_c(self,z_c, c):
        lim=2**8
        if (abs(z_c.x) >= lim ): # if it's big, it's big
            return Coords2D(lim,z_c.y)
        if (abs(z_c.y) >= lim): # if it's big, it's big
            return Coords2D(z_c.x,lim)
        #return Coords2D(z_c.x**2,z_c.y**3)+c
        #to_pow = Coords2D(z_c.y,z_c.x)
        #pow = z_c.complex_pow(self.degree)
        #return Coords2D(abs(pow.x), pow.y)+c
        #return z_c.complex_pow(self.degree) * math.cos(z_c.length() * 4 * math.pi) + c
        #sin: return Coords2D(c.x*math.cos(z_c.length()*math.pi),c.y*math.sin(z_c.length()*math.pi))+c
        #return Coords2D(z_c.x * math.cos(z_c.x * math.pi), z_c.y * math.sin(z_c.y * math.pi)) + c
        #return z_c*(1+math.cos(z_c.length() * math.pi))+c
        #return z_c.complex_pow(self.degree) * math.sin(z_c.x * 4 * math.pi) * math.cos(z_c.y * 4 * math.pi) + c
        try:
            #return z_c.complex_pow(self.degree).complex_cos()+c
            #return z_c.complex_pow(self.degree).complex_cos().complex_sin() + c
            #GOOD #return z_c.complex_pow(self.degree).complex_mul(z_c.complex_cos()) + c
            return z_c.complex_pow(self.degree).complex_mul(z_c.complex_pow(self.degree).complex_cos()) + c
        except OverflowError:
            return z_c

    def no_to_color(self,no):
        return 0 if no.length()<0.5 else 1 if no.length()<1 else 2 \
                    if no.length()<2 else 3 if no.length()<4 else 4 \
                    if no.length() < 8 else 5 if no.length()<16 else 6 \
                    if no.length() < 32 else 7 if no.length()<64 else 8 \
                    if no.length() < 128 else 9

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

        self.z_c = [[self.next_z_c(self.z_c[i][j], self.coords_to_c(Coords2D(j,i))) for j in range(self.field.x)] for i in range(self.field.y)]
        print("For i=10,j=10 c={0},z_c={1}".format(self.coords_to_c(Coords2D(10,10)),self.z_c[10][10]))


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
                color = self.no_to_color(state[i][j])
                #print("Value is {0}, color is {1}".format(state[i][j],self.fill(color)))
                draw.rectangle((begin.x,begin.y,end.x,end.y),fill=self.fill(color))



        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img


