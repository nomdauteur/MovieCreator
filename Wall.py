import random
from copy import deepcopy

from Coords2D import Coords2D

class Wall:
    def __init__(self,start=Coords2D(0,0), end=Coords2D(0,0)):
        self.start = start
        self.end = end
        self.step_vector = deepcopy(self.normal_vector())
        self.set_kind()

    def set_kind(self):
        if (self.start.x==0 and self.end.x==0):
            self._kind="left"
        if (self.start.x>0 and self.end.x>0):
            self._kind= "right"
        if (self.start.y==0 and self.end.y==0):
            self._kind= "upper"
        if (self.start.y>0 and self.end.y>0):
            self._kind= "lower"

    def vector(self):
        return self.end-self.start

    def resize(self,delta):

        self.start += self.step_vector*delta
        self.end += self.step_vector * delta

    def diminish(self,delta):
        v = self.vector()
        if v==Coords2D(0,0):
            return
        self.start += v / v.length() * delta
        self.end -= v / v.length() * delta

    def normal_vector(self):
        v = self.vector()
        if v.length()==0:
            return Coords2D(0,0)
        lengthy_normal=Coords2D(-v.y,v.x)
        return Coords2D(lengthy_normal.x/lengthy_normal.length(),lengthy_normal.y/lengthy_normal.length())

    def kind(self):
        return self._kind


def distance_squared(point=Coords2D(0,0),line=Wall(Coords2D(0,0),Coords2D(0,0))):
    return ((point.x - line.start.x)*(line.end.y-line.start.y) - (point.y - line.start.y)*(line.end.x-line.start.x)) * ((point.x - line.start.x)*(line.end.y-line.start.y) - (point.y - line.start.y)*(line.end.x-line.start.x)) / ((line.end.x-line.start.x)*(line.end.x-line.start.x)+(line.end.y-line.start.y)*(line.end.y-line.start.y))