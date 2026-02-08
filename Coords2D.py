import math
from numbers import Number
from typing import Self

class Coords2D:
    epsilon=1
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if x is None:
            self.x = 0
        if y is None:
            self.y = 0

    def __str__(self):
        return "x: {0}, y: {1}".format(self.x, self.y)

    def __add__(self, other):
        return Coords2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coords2D(self.x - other.x, self.y - other.y)

    def __mul__(self,coefficient: Number) -> Self: # by number
        return Coords2D(self.x*coefficient, self.y*coefficient)

    def complex_mul(self, coord: Self) -> Self: # complex
        return Coords2D(self.x*coord.x - self.y*coord.y, self.y*coord.x + self.x*coord.y)

    def complex_pow(self, power: int):
        if power < 0:
            return None
        if power == 0:
            return Coords2D(1,0)
        res = self
        for i in range(1,power):
            res = res.complex_mul(self)
        #print("power is {0}, start is {1}, finish is {2}".format(power, self,res))
        return res


    def __truediv__(self,coefficient):
        return Coords2D(self.x/coefficient, self.y/coefficient)

    def __eq__(self,other):
        return self.x==other.x and self.y==other.y

    def scalar_product(self,other):
        return self.x*other.x + self.y*other.y

    @staticmethod
    def scalar(a,b):
        return a.x * b.x + a.y * b.y

    @staticmethod
    def point_in_segment(segment_start, segment_end, point):
        if segment_start.x==segment_end.x:
            return (point.x == segment_start.x) and (min(segment_start.y, segment_end.y) <= point.y <= max(segment_start.y, segment_end.y))
        if segment_start.y==segment_end.y:
            return (point.y == segment_start.y) and (min(segment_start.x, segment_end.x) <= point.x <= max(segment_start.x, segment_end.x))
        delta_lambda = (
                    (point.x - segment_start.x) / (segment_end.x - segment_start.x) - (point.y - segment_start.y) / (
                        segment_end.y - segment_start.y))

        if ((-Coords2D.epsilon <= segment_end.x - segment_start.x) and (
                segment_end.x - segment_start.x <= Coords2D.epsilon)):
            return (-Coords2D.epsilon <= point.x - segment_end.x <= Coords2D.epsilon) and (
                    min(segment_start.y, segment_end.y) <= point.y <= max(segment_start.y,
                                                                                segment_end.y))

        if ((-Coords2D.epsilon <= segment_end.y - segment_start.y) and (
                segment_end.y - segment_start.y <= Coords2D.epsilon)):
            return (-Coords2D.epsilon <= point.y - segment_end.y <= Coords2D.epsilon) and (
                    min(segment_start.x, segment_end.x) <= point.x <= max(segment_start.x,
                                                                                segment_end.x))

        return (
                (-Coords2D.epsilon <= delta_lambda) and (delta_lambda <= Coords2D.epsilon)
                and ((point.x - segment_start.x) / (segment_end.x - segment_start.x) >= 0)
                and ((point.x - segment_start.x) / (segment_end.x - segment_start.x) <= 1)
        )

    @staticmethod
    def point_line_distance(point, l1,l2):
        # line is Ax+By+C=0
        A = l2.y-l1.y
        B=l1.x-l2.x
        C=-(A*l1.x+B*l1.y)
        if (A==0 and B==0):
            return 0
        return (math.fabs(A*point.x+B*point.y+C))/(math.sqrt(A*A+B*B))

    @staticmethod
    def segments_intersect(A,B,C,D):
        # Line AB represented as a1x + b1y = c1
        a1 = B.y - A.y
        b1 = A.x - B.x
        c1 = a1 * (A.x) + b1 * (A.y)

        # Line CD represented as a2x + b2y = c2
        a2 = D.y - C.y
        b2 = C.x - D.x
        c2 = a2 * (C.x) + b2 * (C.y)

        determinant = a1 * b2 - a2 * b1

        if (determinant != 0):
            x = (b2 * c1 - b1 * c2) / determinant
            y = (a1 * c2 - a2 * c1) / determinant

            result=Coords2D(x,y)

            if (Coords2D.point_in_segment(A, B, result) and Coords2D.point_in_segment(C, D, result)):
                return result
        return Coords2D(10 ** 9, 10 ** 9)

    def length(self):
        #print("{0},{1} gives length {2}".format(self.x,self.y,math.sqrt(self.x*self.x + self.y*self.y)))
        return math.sqrt(self.x*self.x + self.y*self.y)

    def angle(self,other):
        return math.acos(self.scalar_product(other)/(self.length()*other.length()))


    @staticmethod
    def exists(pointer, size):
        return 0<=pointer.x<size.x and 0<=pointer.y<size.y

    def exists_between(pointer, size):
        return size[0]<=pointer.x<size[2] and size[1]<=pointer.y<size[3]

    @staticmethod
    def turn(vector, angle,start_point=None): # angle in rads
        if start_point is None:
            start_point = Coords2D(0, 0)
        angle = - angle # computer axis
        return (start_point+
                Coords2D(vector.x*math.cos(angle) - vector.y*math.sin(angle), vector.x*math.sin(angle) + vector.y*math.cos(angle)))

    @staticmethod
    def point_between(point1, point2, lyambda):
        return point1+(point2-point1)*lyambda

    @staticmethod
    def make_regular_polygon(vertices_no, center, radius):
        angle=math.pi*2/vertices_no
        points=[]
        for i in range(vertices_no):
            points.append(center + Coords2D(-math.sin(angle*(0.5+i)),math.cos(angle*(0.5+i)))*radius)
        return points
