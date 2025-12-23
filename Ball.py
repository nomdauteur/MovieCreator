import random
from Coords2D import Coords2D
from Wall import Wall, distance_squared


class Ball:

    epsilon=1

    def __init__(self,radius=5, spawn_point=Coords2D(0,0), acceleration=0):
        self.radius = radius
        self.spawn_point = spawn_point
        self.current_point=self.spawn_point
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.speed=Coords2D(random.randint(50,300),random.randint(50,300))
        self.acceleration=Coords2D(0,acceleration)

    def add_force(self, force=Coords2D(0,0)):
        self.acceleration=self.acceleration+force

    def change_size(self,delta):
        self.radius+=delta

    def change_color(self,delta):
        self.color=((self.color[0]+delta[0])%255,(self.color[1]+delta[1])%255,(self.color[2]+delta[2])%255)

    def step(self,time_unit,walls):
        should=False
        bounceable_wall=None
        walls_count=0
        for wall in walls:
            if (self.should_bounce(wall,time_unit)):
                walls_count+=1
                should=True
                bounceable_wall=wall

        self.current_point=self.current_point+self.speed*time_unit
        self.speed=self.speed+self.acceleration*time_unit
        if walls_count>1:
            print("Ball hit a corner, reflecting")
            self.reflect()
            self.change_color((255-2*self.color[0]+random.randint(-10,10),255-2*self.color[1]+random.randint(-10,10),255-2*self.color[2]+random.randint(-10,10)))
        elif (bounceable_wall is not None):
            print("Ball with radius {0} standing on ({2},{3})will bounce from the {1} wall".format(self.radius,bounceable_wall.kind(),self.current_point.x,self.current_point.y))
            self.bounce(bounceable_wall)
            self.change_color((255-2*self.color[0]+random.randint(-10,10),255-2*self.color[1]+random.randint(-10,10),255-2*self.color[2]+random.randint(-10,10)))
        self.unhole(walls)

    def unhole(self,walls):
        field_x=0
        field_y=0
        for w in walls:
            field_x=max(field_x,w.start.x,w.end.x)
            field_y = max(field_y, w.start.y, w.end.y)
        self.current_point = Coords2D(min(max(self.radius, self.current_point.x), field_x-self.radius),
                                      min(max(self.radius, self.current_point.y), field_y-self.radius))



    def bounce(self, wall):
        #print("LOG: Ball bounces, speed now: {0},{1}".format(self.speed.x,self.speed.y) )
        self.speed=self.speed-wall.normal_vector()*2*Coords2D.scalar_product(self.speed,wall.normal_vector())
        #print("LOG: Ball bounced, speed now: {0},{1}".format(self.speed.x, self.speed.y))
    def reflect(self):
        #print("LOG: Ball bounces, speed now: {0},{1}".format(self.speed.x,self.speed.y) )
        self.speed=self.speed * -1
        #print("LOG: Ball bounced, speed now: {0},{1}".format(self.speed.x, self.speed.y))

    def should_bounce(self, wall, time_unit):
        next_place=self.current_point+self.speed*time_unit

        # for now consider walls as borders strictly
        kind = wall.kind()
        #print("{0} wall".format(kind))
        return ((kind == "left" and next_place.x-self.radius < Ball.epsilon)
                or (kind == "right" and next_place.x+self.radius > Ball.epsilon + wall.start.x)
                or (kind == "upper" and next_place.y-self.radius < Ball.epsilon)
                or (kind == "lower" and next_place.y+self.radius > Ball.epsilon + wall.start.y)
                )
        """intersection=Coords2D.segments_intersect(self.current_point,next_place, wall.start,wall.end)
        if (intersection.x!=10**9):
            return intersection
        return Coords2D(10**9,10**9)"""


