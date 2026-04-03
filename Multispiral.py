import math
from copy import deepcopy

from Drawer import Drawer
from Coords2D import Coords2D
from PIL import Image, ImageDraw, ImageFont


class Spiral():
    def __init__(self, b, speed, parent_id, born_time):
        self.b = b
        self.speed = speed
        self.parent_id = parent_id
        self.born_time = born_time
    def get_age(self,curr_time):
        return curr_time-self.born_time
    def get_offset(self, curr_time): # center moves, so offset from it
        age = self.get_age(curr_time)
        r = self.b * age
        phi = age * self.speed / 180 * math.pi
        return Coords2D(math.cos(phi), math.sin(phi)) * r

class Multispiral(Drawer):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,
                 ):
        super().__init__(size, length, rate, field_size, border)

        self.time=0
        self.init_speed = 72/self.rate
        self.init_b = self.field.x / 2 / self.length / self.rate / 1.1

        self.center = Coords2D(self.field.x/2,self.field.y/2)

        self.spirals = [Spiral(self.init_b,self.init_speed, None,0)]

    def get_current_point(self, id, curr_time, max_time):
        s = self.spirals[id]
        if (s.parent_id is None):
            center = self.center
        else:
            center = self.get_current_point(s.parent_id,max_time,max_time)

        sgn = (-1)**id
        off = s.get_offset(curr_time)
        return center + Coords2D(sgn*off.x,off.y)



    def next_state(self):
        print("Plus state")

        self.time+=1

        if (self.time ==10):
            self.spirals.append(Spiral(self.init_b/6, self.init_speed*1.9, 0, self.time))

        #return {"time":deepcopy(self.time), "points":deepcopy([self.get_current_point(id) for id in range (len(self.spirals))])}
        return {"time": deepcopy(self.time)}


    def get_all_states(self):
        #self.states=[{"time":0, "points":[self.center]}]
        self.states = [{"time": 0}]

        for i in range(self.length*self.rate):
            self.states.append(deepcopy(self.next_state()))


    def draw_image(self, state, size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x, size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        colors = ["red","green","blue"]

        self.compute_scale(size)
        #print(state)
        for i in range(state["time"]):
            for s in range(len(self.spirals)):
                if (self.spirals[s].born_time>i):
                    continue
                begin = self.offset_point(self.get_current_point(s,i,state["time"]))
                end = self.offset_point(self.get_current_point(s,i+1,state["time"]))
                draw.line((begin.x,begin.y,end.x,end.y), fill=colors[s%3], width=math.floor(5/(s+1)))
            #curr = self.offset_point(state["points"][-1])
            #draw.circle((curr.x,curr.y),radius=5, fill="red")


        if (self.border):
            self.draw_border(draw)

        self.watermark(draw)

        return img


