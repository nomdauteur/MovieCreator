from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D

class DragonCurve(PolyLineDrawer):

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, init_point=Coords2D(0,0)):
        super().__init__(size, length, rate, field_size, border)
        self.poly_lines[0]=init_point
        self.direction=Coords2D(1,0)
        self.axiom, self.tempAx, self.logic, self.count = 'FX', '', {'X': 'X+YF+', 'Y': '−FX−Y'}, 15
        for i in range(self.count):
            for j in self.axiom:
                self.tempAx += self.logic[j] if j in self.logic else j
            self.axiom, self.tempAx = self.tempAx, ''
            self.axiom_counter=0

    def step(self, direction):
        new_cell=self.poly_lines[-1]+direction
        if not Coords2D.exists(new_cell, self.field):
            if (new_cell.x>=self.field.x):
                self.field.x+=1
                self.matrix=[row + [0] for i, row in enumerate(self.matrix)]

            if (new_cell.x<0):
                self.field.x+=1
                self.matrix=[ [0]+ row for i, row in enumerate(self.matrix)]
                for i in self.poly_lines:
                    i.x+=1
            if (new_cell.y>=self.field.y):
                self.field.y+=1
                self.matrix.append([0 for i in range(self.field.x)])
            if (new_cell.y<0):
                self.field.y+=1
                self.matrix.insert(0,[0 for i in range(self.field.x)])
                for i in self.poly_lines:
                    i.y+=1
            new_cell = self.poly_lines[-1] + direction
            #self.compute_scale()
        self.poly_lines.append(new_cell)
        self.matrix[self.poly_lines[-1].y][self.poly_lines[-1].x] = 1


    def next_state(self):
        if (self.axiom_counter < len(self.axiom)):
            match self.axiom[self.axiom_counter]:
                case 'F':
                    self.step(self.direction)
                case '+':
                    self.direction=Coords2D(-self.direction.y, self.direction.x)
                case '−':
                    self.direction=Coords2D(self.direction.y, -self.direction.x)
            self.axiom_counter+=1
        return {"lines":self.poly_lines,"current_field_size":self.field}