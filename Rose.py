import math
from PointyDraw import PointyDraw
from Coords2D import Coords2D


class Rose(PointyDraw):
    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, need_grid=False, k=1):
        super().__init__(size, length, rate, field_size, border,need_grid)
        self.k=k

    def continue_condition(self):
        return (self.k*self.phi <=2*math.pi)

    def next_point(self,center,radius):
        print("Phi is: {0} pi".format(self.phi/math.pi))
        point_real = center + Coords2D(radius * math.cos(self.phi*self.k)*math.cos(self.phi),
                                       radius * math.cos(self.phi*self.k)*math.sin(self.phi))
        point = Coords2D(math.floor(point_real.x), math.floor(point_real.y))
        return {"real":point_real,"int":point}

