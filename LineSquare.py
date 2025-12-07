import random
from copy import deepcopy

from PIL import Image, ImageDraw, ImageFont

from Coords2D import Coords2D
from PolyLineDrawer import PolyLineDrawer

class LineSquare(PolyLineDrawer):

    def __init__(self,size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100),
                 border=False, side=2):
        super().__init__(size, length, rate, field_size, border)
        self.side=side

    def get_square(self,i,j):
        result=[]
        square_side=min(self.field.x,self.field.y)/self.side
        left_upper=Coords2D(j*square_side,i*square_side)
        right_bottom = Coords2D((j+1) * square_side, (i+1) * square_side)
        center=Coords2D((j+0.5)*square_side, (i+0.5) * square_side)
        #first quarter
        x = right_bottom.x
        curr_y=right_bottom.y
        while(curr_y>left_upper.y):
            delta=random.randint(5,20)
            curr_y-=delta
            result.append(Coords2D(x,max(curr_y,left_upper.y)))
        print("One side off")
        #second quarter
        y = left_upper.y
        curr_x = right_bottom.x
        while (curr_x > left_upper.x):
            delta=random.randint(5,20)
            curr_x -= delta
            result.append(Coords2D(max(curr_x,left_upper.x), y))
        print("Second side off")
        #third quarter
        x = left_upper.x
        curr_y = left_upper.y
        while (curr_y < right_bottom.y):
            delta=random.randint(5,20)
            curr_y += delta
            result.append(Coords2D(x, min(curr_y,right_bottom.y)))
        print("Third side off")
        #fourth quarter
        y = right_bottom.y
        curr_x = left_upper.x
        while (curr_x < right_bottom.x):
            delta=random.randint(5,20)
            curr_x += delta
            result.append(Coords2D(min(curr_x,right_bottom.x), y))
        print("Square off")


        return {"result":result,"center":center}


    def get_all_states(self):
        curr_state = []
        for i in range(0, self.side):
            for j in range(0, self.side):
                square = self.get_square(i,j)
                center=square["center"]
                for r in square["result"]:
                    end_point=Coords2D.point_between(center,r,random.uniform(0.7,1))
                    curr_state.append({"line":[center.x,center.y,end_point.x,end_point.y],"width":random.randint(1,5)})
                    self.states.append(deepcopy(curr_state))

        return self.states

    def grid(self,draw):
        for i in range(self.side+1):
            draw.line([self.offset.x,
                       self.offset.y + i *(self.field.x/self.side)* self.multiplier,
                       self.offset.x + self.field.x * self.multiplier,
                       self.offset.y + i *(self.field.x/self.side)* self.multiplier], fill="black", width=2)

        for i in range(self.side+1):
            draw.line([self.offset.x + i*(self.field.x/self.side) * self.multiplier,
                       self.offset.y,
                       self.offset.x + i*(self.field.x/self.side) * self.multiplier,
                       self.offset.y + self.field.y * self.multiplier], fill="black", width=2)


    def draw_image(self,state,size=None):
        if size is None:
            size = Coords2D(self.size.x, self.size.y)
        img = Image.new("RGB", (size.x,size.y), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        self.compute_scale(size,self.field)

        for line in state:
            draw.line([self.offset.x+self.multiplier*line["line"][0],self.offset.y+self.multiplier*line["line"][1],
                           self.offset.x+self.multiplier*line["line"][2],self.offset.y+self.multiplier*line["line"][3]],fill="black",width=line["width"])
        if (self.border):
            self.draw_border(draw)

        self.grid(draw)
        return img

        self.watermark(draw)

        return img
