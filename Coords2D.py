import math


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
        return math.sqrt(self.x*self.x + self.y*self.y)

    def angle(self,other):
        return math.acos(self.scalar_product(other)/(self.length()*other.length()))

    def __mul__(self,coefficient): # by number
        return Coords2D(self.x*coefficient, self.y*coefficient)