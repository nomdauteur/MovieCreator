import math
from copy import deepcopy

from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D


class Gosper(PolyLineDrawer):

    @staticmethod
    def num_to_color(num):
        return (0,0,0)

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False,
                 init_point=Coords2D(0, 0)):
        super().__init__(size, length, rate, field_size, border)
        self.poly_lines[0] = init_point
        self.direction = Coords2D(0, -1)
        self.axiom, self.tempAx, self.logic, self.count = 'A', '', {'A': 'A-B--B+A++AA+B-', 'B': '+A-BB--B-A++A+B'}, 4
        for i in range(self.count):
            for j in self.axiom:
                self.tempAx += self.logic[j] if j in self.logic else j
            self.axiom, self.tempAx = self.tempAx, ''
            self.axiom_counter = 0
        print("Grammar is:")
        print(self.axiom)

    def step(self, direction):
        new_cell = self.poly_lines[-1] + direction
        if not Coords2D.exists(new_cell, self.field):
            if (new_cell.x >= self.field.x):
                self.field.x += 1
                #self.matrix = [row + [0] for i, row in enumerate(self.matrix)]

            if (new_cell.x < 0):
                self.field.x += 1
                #self.matrix = [[0] + row for i, row in enumerate(self.matrix)]
                for i in self.poly_lines:
                    i.x += 1
            if (new_cell.y >= self.field.y):
                self.field.y += 1
                #self.matrix.append([0 for i in range(self.field.x)])
            if (new_cell.y < 0):
                self.field.y += 1
                #self.matrix.insert(0, [0 for i in range(self.field.x)])
                for i in self.poly_lines:
                    i.y += 1
            new_cell = self.poly_lines[-1] + direction
            # self.compute_scale()
        self.poly_lines.append(new_cell)
        #self.matrix[self.poly_lines[-1].y][self.poly_lines[-1].x] = 1

    def get_all_states(self): #not by hard time but by ending of figure
        while(self.axiom_counter < len(self.axiom)):
            self.states.append(deepcopy(self.next_state()))

    def next_state(self):
        if (self.axiom_counter < len(self.axiom)):
            match self.axiom[self.axiom_counter]:
                case '+':
                    self.direction = Coords2D.turn(self.direction,math.pi/3, None)
                case '-':
                    self.direction = Coords2D.turn(self.direction,-math.pi/3, None)

                case _:
                    self.step(self.direction)
            self.axiom_counter += 1
        return {"lines": self.poly_lines, "current_field_size": self.field}