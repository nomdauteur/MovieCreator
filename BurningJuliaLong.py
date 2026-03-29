import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont


class BurningJuliaLong(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,
                 degree=2):
        super().__init__(size, length, rate, field_size, border)
        self.degree = degree
        self.c = None
        self.z_start = [[self.coords_to_z(Coords2D(j,i)) for j in range(self.field.x)] for i in range(self.field.y)]
        #self.colors = [[8 for j in range(self.field.x)] for i in range(self.field.y)]
        self.file_name = "videos/"+"BurningJuliaLong_"+str(self.degree)+"_"

        self.iterations_no=10

    def z_to_coords(self, z):
        return (z + Coords2D(self.field.x/1.67, self.field.y/2)) * self.field.x/4

    def coords_to_z(self,coords):
        return (coords - Coords2D(self.field.x / 1.67, self.field.y / 2)) /self.field.x*4

    def next_z_c(self,z_c, c):
        if (abs(z_c.x) > 2**8 ): # if it's big, it's big
            return Coords2D(2**8,z_c.y)
        if (abs(z_c.y) > 2**8): # if it's big, it's big
            return Coords2D(z_c.x,2**8)
        to_pow = Coords2D(abs(z_c.x), abs(z_c.y))
        return to_pow.complex_pow(self.degree) + c
        return to_pow.complex_pow(self.degree)+c

    def no_to_color(self,no):
        return 0 if no.length()<0.5 else 1 if no.length()<1 else 2 \
                    if no.length()<2 else 3 if no.length()<4 else 4 \
                    if no.length() < 8 else 5 if no.length()<16 else 6 \
                    if no.length() < 32 else 7 if no.length()<64 else 8 \
                    if no.length() < 128 else 9

    def get_colors(self, c):
        z_c = self.z_start
        for k in range(self.iterations_no):
            z_c=[[self.next_z_c(z_c[i][j],c) for j in range(self.field.x)] for i in range(self.field.y)]
        return [[self.no_to_color(z_c[i][j]) for j in range(self.field.x)] for i in range(self.field.y)]


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
        print("c equals {0} + {1} i".format(self.c.x, self.c.y))
        return {"c":deepcopy(self.c),"colors":deepcopy(self.get_colors(self.c))}


    def get_all_states(self):
        for r in range(2,12):
            for phi in range(1,361, 10):
                phi_rad = phi / 180 * math.pi
                self.c = Coords2D(math.cos(phi_rad), math.sin(phi_rad)) * r / 10
                self.states.append(deepcopy(self.next_state()))

    def draw_image(self, state, size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x, size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.compute_scale(size)
        #print(state)
        text_point = Coords2D(180, 200)
        font = ImageFont.truetype("segoesc.ttf", 20)
        sgn = " + " if state["c"].y>0 else " "
        draw.text((text_point.x, text_point.y),
                  "c = " + str(round(state["c"].x,3)) +sgn+ str(round(state["c"].y,3))+" i", font=font, fill="black")

        for i in range(self.field.x):
            for j in range(self.field.y):
                begin = self.offset_point(Coords2D(j,i))
                end = self.offset_point(Coords2D(j+1, i+1))
                color = state["colors"][i][j]
                draw.rectangle((begin.x,begin.y,end.x,end.y),fill=self.fill(color))



        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        img.save("videos/"+"BurningJuliaLong_"+str(state["c"].x)+"_"+str(state["c"].y)+".jpg")

        return img


