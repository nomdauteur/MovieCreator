from Drawer import Drawer
from Coords2D import Coords2D

import random
from copy import deepcopy

class GameOfLifeDrawer(Drawer):

    @staticmethod
    def num_to_color(num):
        return (255,255,255) if num==1 else (43,44,90)

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100), border=False, births=[3], stables=[2,3], initial_state=None):
        super().__init__(size, length, rate, field_size,border)
        self.births=births
        self.stables=stables
        if initial_state is None:
            initial_state = [[0 for _ in range(self.field.x)] for _ in range(self.field.y)]
            for i in range(0, self.field.y):
                for j in range(0, self.field.x):
                    initial_state[i][j]=random.randint(0,1)

        self.initial_state = deepcopy(initial_state)
        self.current_state=deepcopy(self.initial_state)

    def count_neighbors(self, i, j, state):
        res = 0
        for a in range(-1,2):
            for b in range(-1,2):
                if (a == 0 and b == 0) :
                    continue
                if (i + a < 0 or i + a >= self.field.y or j + b < 0 or j + b >= self.field.x):
                    continue
                res += state[i+a][j+b]
        return res

    def next_state(self):
        self.time+=1
        tmp_state = deepcopy(self.current_state)
        for i in range(0, self.field.y):
            for j in range(0, self.field.x):
                n = self.count_neighbors(i, j, tmp_state)
                if (n in self.births):
                    self.current_state[i][j] = 1
                elif (n in self.stables):
                    continue
                else:
                    self.current_state[i][j] = 0

        return self.current_state