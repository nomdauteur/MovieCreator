import random
from Coords2D import Coords2D

class Wall:
    def __init__(self,start=Coords2D(0,0), end=Coords2D(0,0)):
        self.start = start
        self.end = end

    def vector(self):
        return self.end-self.start

    def normal_vector(self):
        v = self.vector()
        lengthy_normal=Coords2D(-v.y,v.x)
        return Coords2D(lengthy_normal.x/lengthy_normal.length(),lengthy_normal.y/lengthy_normal.length())

    def kind(self):
        if (self.start.x==0 and self.end.x==0):
            return "left"
        if (self.start.x>0 and self.end.x>0):
            return "right"
        if (self.start.y==0 and self.end.y==0):
            return "upper"
        if (self.start.y>0 and self.end.y>0):
            return "lower"

def distance_squared(point=Coords2D(0,0),line=Wall(Coords2D(0,0),Coords2D(0,0))):
    return ((point.x - line.start.x)*(line.end.y-line.start.y) - (point.y - line.start.y)*(line.end.x-line.start.x)) * ((point.x - line.start.x)*(line.end.y-line.start.y) - (point.y - line.start.y)*(line.end.x-line.start.x)) / ((line.end.x-line.start.x)*(line.end.x-line.start.x)+(line.end.y-line.start.y)*(line.end.y-line.start.y))