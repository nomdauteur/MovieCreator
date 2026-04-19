from Drawer import Drawer
from Coords2D import Coords2D

import random
from copy import deepcopy

class MultiGameOfLife(Drawer):

    @staticmethod
    def num_to_color(num):
        colors=["white","green","blue","orange","brown"]
        return colors[num]

    def __init__(self, size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100),
                 border=False, agents=[{"births":[3],"stable":[2,3]}, {"births":[3],"stable":[2,3]}, {"births":[3],"stable":[2,3]}], initial_state=None):
        super().__init__(size, length, rate, field_size,border)
        self.agents = agents

        if initial_state is None:
            initial_state = [[0 for _ in range(self.field.x)] for _ in range(self.field.y)]
            for i in range(0, len(self.agents)):
                rand_x=random.randint(3,self.field.y-4)
                rand_y=random.randint(3,self.field.x-4)
                initial_state[rand_x+1][rand_y-1] = (i+1) *  random.randint(0,1)
                initial_state[rand_x+1][rand_y+3] = (i+1) *  random.randint(0,1)
                initial_state[rand_x-1][rand_y+1] = (i+1) *  random.randint(0,1)
                initial_state[rand_x+3][rand_y+1] = (i+1) *  random.randint(0,1)
                initial_state[rand_x][rand_y]=i+1
                initial_state[rand_x][rand_y+1] = (i+1) *  random.randint(0,1)
                initial_state[rand_x+1][rand_y] = (i+1) *  random.randint(0,1)
                initial_state[rand_x+1][rand_y+1] = (i+1) *  random.randint(0,1)
                initial_state[rand_x][rand_y+2] = (i+1) *  random.randint(0,1)
                initial_state[rand_x+1][rand_y+2] = (i+1) *  random.randint(0,1)
                initial_state[rand_x+2][rand_y] = (i+1) *  random.randint(0,1)
                initial_state[rand_x+2][rand_y+1] = (i+1) *  random.randint(0,1)
                initial_state[rand_x+2][rand_y+2] = (i+1) *  random.randint(0,1)

        self.initial_state = deepcopy(initial_state)
        self.current_state=deepcopy(self.initial_state)
        self.should_continue=True

    def count_neighbors(self, i, j, state, color):
        res = 0
        for a in range(-1,2):
            for b in range(-1,2):
                if (a == 0 and b == 0) :
                    continue
                if (i + a < 0 or i + a >= self.field.y or j + b < 0 or j + b >= self.field.x):
                    continue
                if (state[i+a][j+b] == color):
                    res += 1
        return res

    def next_state(self):
        self.time+=1
        self.should_continue=False

        for c in range(1, len(self.agents) + 1):
            tmp_state = deepcopy(self.current_state)
            for i in range(0, self.field.y):
                for j in range(0, self.field.x):
                    if (tmp_state[i][j]!=0 and tmp_state[i][j]!=c):
                        #print("A{0}.{1}".format(i,j))
                        continue
                    n = self.count_neighbors(i, j, tmp_state, c)
                    if (tmp_state[i][j]==0 and n in self.agents[c-1]["births"]):
                        self.should_continue=True
                        #print("birthing {0}".format(self.num_to_color(c)))
                        self.current_state[i][j] = c
                    elif (n in self.agents[c-1]["stable"]):
                        continue
                    else:

                        self.current_state[i][j] = 0


        return self.current_state


    def get_all_states(self):
        self.states = [deepcopy(self.current_state)]
        cnt=0
        while(self.should_continue):
            self.states.append(deepcopy(self.next_state()))
            cnt+=1
            if (cnt%10==0):
                print("{0}th cadre".format(cnt))