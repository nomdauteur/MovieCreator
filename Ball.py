import random
from Coords2D import Coords2D
from Wall import Wall, distance_squared


class Ball:

    epsilon=5

    def __init__(self,radius=5, spawn_point=Coords2D(0,0), acceleration=0):
        self.radius = radius
        self.spawn_point = spawn_point
        self.current_point=self.spawn_point
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.speed=Coords2D(random.randint(5,300),random.randint(5,300))
        self.acceleration=Coords2D(0,acceleration)

    def add_force(self, force=Coords2D(0,0)):
        self.acceleration=self.acceleration+force

    def step(self,time_unit,walls):
        should=False
        bounceable_wall=None
        for wall in walls:
            if (self.should_bounce(wall,time_unit)):
                should=True
                bounceable_wall=wall
                break
        self.current_point=self.current_point+self.speed*time_unit
        self.speed=self.speed+self.acceleration*time_unit
        if (bounceable_wall is not None):
            self.bounce(bounceable_wall)

    def bounce(self, wall):
        #print("LOG: Ball bounces, speed now: {0},{1}".format(self.speed.x,self.speed.y) )
        self.speed=self.speed-wall.normal_vector()*2*Coords2D.scalar_product(self.speed,wall.normal_vector())
        #print("LOG: Ball bounced, speed now: {0},{1}".format(self.speed.x, self.speed.y))

    def should_bounce(self, wall, time_unit):
        next_place=self.current_point+self.speed*time_unit

        # for now consider walls as borders strictly
        kind = wall.kind()
        return ((kind == "left" and next_place.x-self.radius < Ball.epsilon)
                or (kind == "right" and next_place.x+self.radius > Ball.epsilon + wall.start.x)
                or (kind == "upper" and next_place.y-self.radius < Ball.epsilon)
                or (kind == "lower" and next_place.y+self.radius > Ball.epsilon + wall.start.y)
                )
        """intersection=Coords2D.segments_intersect(self.current_point,next_place, wall.start,wall.end)
        if (intersection.x!=10**9):
            return intersection
        return Coords2D(10**9,10**9)"""


