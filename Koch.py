from PolyLineDrawer import PolyLineDrawer
from Coords2D import Coords2D
import math

class Koch(PolyLineDrawer):

    def __init__(self,size=Coords2D(1920, 800), length=60, rate=1, field_size=Coords2D(100, 100),
                 border=False, side=2, max_iterations=0):
        super().__init__(size, length, rate, field_size, border)
        self.side=side
        self.poly_lines=[]
        self.iter_no=0
        for i in range(side):
            for j in range(side):
                #triangle
                side_x = self.field.x/side
                side_y = self.field.y / side
                self.poly_lines.append(Coords2D(j*side_x+side_x/20,i*side_y+side_y*9/10))
                self.poly_lines.append(Coords2D(j*side_x+side_x/2,(i+1)*side_y-243/400*side_y*side_y-side_y/10))
                self.poly_lines.append(Coords2D(j*side_x+19*side_x/20,i*side_y+side_y*9/10))

    def get_all_states(self):
        for i in range(0, self.max_iterations + 1):
            self.states.append(deepcopy(self.next_state()))

    def next_state(self):
        new_poly_lines=[]
        for i in range (len(self.poly_lines)-1):
            first_point=self.poly_lines[i]
            fifth_point=self.poly_lines[i+1]
            second_point=Coords2D(first_point.x+1/3*(fifth_point.x-first_point.x),first_point.y+1/3*(fifth_point.y-first_point.y))
            rotable_vector=second_point-first_point
            third_point=second_point + Coords2D(rotable_vector.x*(-1/2)-rotable_vector.y*math.pow(3,1/2)/2,-rotable_vector.y*1/2+rotable_vector.x*math.pow(3,1/2)/2)
            fourth_point=Coords2D(first_point.x+2/3*(fifth_point.x-first_point.x),first_point.y+2/3*(fifth_point.y-first_point.y))
            new_poly_lines.extend([self.poly_lines[i],second_point,third_point,fourth_point,self.poly_lines[i+1]])
        self.poly_lines=new_poly_lines
        return {"lines":self.poly_lines,"current_field_size":self.field}
