import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont


class BurningShip(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,
                 degree=2,start=Coords2D(0,0)):
        super().__init__(size, length, rate, field_size, border)
        self.degree = degree
        self.start = start
        self.z_c = [[self.start for _ in range(self.field.x)] for _ in range(self.field.y)]
        self.file_name="videos/BurningShip_"+str(self.degree)+"_"

    def c_to_coords(self, c):
        return (c + Coords2D(self.field.x/1.67, self.field.y/2)) * self.field.x / 4

    def coords_to_c(self,coords):
        return (coords - Coords2D(self.field.x / 1.67, self.field.y / 2)) /self.field.x * 4

    def next_z_c(self,z_c, c):
        if (abs(z_c.x) >= 2**7 ): # if it's big, it's big
            return Coords2D(2**7,z_c.y)
        if (abs(z_c.y) >= 2**7): # if it's big, it's big
            return Coords2D(z_c.x,2**7)
        to_pow = Coords2D(abs(z_c.x),abs(z_c.y))
        return to_pow.complex_pow(self.degree)+c

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
                color = 0 if state[i][j].length()<0.25 else 1 if state[i][j].length()<0.5 else 2 \
                    if state[i][j].length()<1 else 3 if state[i][j].length()<2 else 4 \
                    if state[i][j].length() < 2**2 else 5 if state[i][j].length()<2**3 else 6 \
                    if state[i][j].length() < 2**4 else 7 if state[i][j].length()<2**5 else 8 \
                    if state[i][j].length() < 2 ** 6 else 9
                #print("Value is {0}, color is {1}".format(state[i][j],self.fill(color)))
                draw.rectangle((begin.x,begin.y,end.x,end.y),fill=self.fill(color))



        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img


