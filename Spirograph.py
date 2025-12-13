import math
from PointyDraw import PointyDraw
from Coords2D import Coords2D


class Spirograph(PointyDraw):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, need_grid=True, k=0.99,l=0.99):
        super().__init__(size, length, rate, field_size, border,need_grid)
        self.k=k
        self.l=l
        self.file_name = "videos/spirograph_" +"K"+str(self.k)+"L"+str(self.l)

    def continue_condition(self):
        return (self.k*self.phi <=10*math.pi)

    def next_point(self,center,radius):
        print("Here Phi is: {0} pi".format(self.phi/math.pi))

        point_real = center + Coords2D(  (1.0-self.k)*math.sin(self.k*self.phi)- self.l*math.sin(self.phi) ,
                                       -(1.0-self.k)*math.cos(self.k*self.phi)- self.l*math.cos(self.phi )) * radius
        point = Coords2D(math.floor(point_real.x), math.floor(point_real.y))
        return {"real":point_real,"int":point}

