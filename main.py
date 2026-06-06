import os
import math
import random
import GameOfLifeDrawer
import Drawer
import BallDrawer
import PolyLineDrawer
from Coords2D import Coords2D
import DragonCurve
import Koch
import Gosper
import Levy
import LongLevyByAngle
import Cesaro
import TSquare
import HSquare
import Spiral
import LineSquare
import MonteCarlo
import PointyDraw
import Rose
import MaurerRose
import Spirograph
import Harmonograph
import ChaosGame
import TimesCircle
import GrowingBallDrawer
import ShrinkingWallDrawer
import CollidingSpawnDrawer
import MarchingSquares
import Limason
import ExpoCircle
import ExponentCircle
import LongExpoCircle
import LongExponentCircle
import Pendulums
import Mandelbrot
import Julia
import JuliaLong
import LongGameOfLifeDrawer
import Methuselahs
import BurningShip
import BurningJuliaLong
import BurningJulia
import Multispiral
import Voronoi
import MultiGameOfLife
import ExperimentJuliaLong
import ExperimentMandelbrot
import ExperimentJulia

height=1920
width=800
'''
init_state=[[0 for _ in range(200)] for _ in range(200)]
for i in range(0,40):
    rand=random.randint(0,5)
    if (rand==1):
        for a in range(0,5):
            for b in range(0, 5):
                init_state[5*i+a][5*i+b]=random.randint(0,1)
'''

#drawer = GameOfLifeDrawer.GameOfLifeDrawer(Coords2D(1080,1920),15,30,Coords2D(200,200), True,births=[3],stables=[0,1,2,3,4,5,6,7,8],initial_state=init_state)
#drawer = Drawer.Drawer((600,1000),10,1,(20,20))
#drawer=BallDrawer.BallDrawer(Coords2D(1080,1920), 60, Coords2D(500,700),20,True,100)
#drawer=PolyLineDrawer.PolyLineDrawer(Coords2D(800,1920), 10, 10, Coords2D(20,20),True)

#drawer= Koch.Koch(Coords2D(1080,1920), 3, 1, field_size=Coords2D(400,400),border=True,side=1,max_iterations=7)


#drawer= Cesaro.Cesaro(Coords2D(1080,1920), 3, 1, field_size=Coords2D(1080,1080),border=False,max_iterations=7)
#drawer=TSquare.TSquare(Coords2D(1080,1920), 30, 2, field_size=Coords2D(1080,1080),border=False,max_iterations=8)
#drawer=HSquare.HSquare(Coords2D(1080,1920), 30, 2, field_size=Coords2D(1080,1080),border=False,max_iterations=8)
#drawer=Spiral.Spiral(Coords2D(1080,1920), 30, 10, field_size=Coords2D(200,200),border=True)
#drawer=LineSquare.LineSquare(Coords2D(1080,1920), 30, 30, field_size=Coords2D(500,500),border=False,side=5)
#drawer=PointyDraw.PointyDraw(Coords2D(1080,1920), 30, 100, field_size=Coords2D(40,40),border=False)
#drawer=Rose.Rose(Coords2D(1080,1920), 30, 100, field_size=Coords2D(200,200),border=False,k_up=4,k_down=9)
#drawer=MaurerRose.MaurerRose(Coords2D(1080,1920), 30, 50, field_size=Coords2D(200,200),border=False,n=6,d=71)
#drawer=Spirograph.Spirograph(Coords2D(1080,1920), 30, 300, field_size=Coords2D(200,200),border=False,k=0.0967,l=0.441)
#drawer=Harmonograph.Harmonograph(Coords2D(1080,1920), 30, 100, field_size=Coords2D(500,500),border=False, a=[1,0,1,0],f=[70.1,0,10.1,0],p=[1.2,0,15.1,0],d=[0.5,0,0.04,0])
#a=[1,0,1,0],f=[10.1,0,60.1,0],p=[1.2,0,15.1,0],d=[0.005,0,0.04,0] - sharp pikes
#a=[1,0,1,0],f=[70.1,0,10.1,0],p=[1.2,0,15.1,0],d=[0.5,0,0.04,0] - VASE

#drawer=ShrinkingWallDrawer.ShrinkingWallDrawer(Coords2D(1080,1920), 60, Coords2D(500,500),20,False,100)
#drawer=CollidingSpawnDrawer.CollidingSpawnDrawer(Coords2D(1080,1920), 30, Coords2D(500,500),20,False,100)

#drawer=GrowingBallDrawer.GrowingBallDrawer(Coords2D(1080,1920), 60, Coords2D(500,500),32,False,100)
#drawer=Gosper.Gosper(Coords2D(1080,1920), 30, 512, field_size=Coords2D(20,20),border=True,init_point=Coords2D(0,10))
#drawer=DragonCurve.DragonCurve(Coords2D(1080,1920), 60, 128, field_size=Coords2D(30,30),border=True,init_point=Coords2D(5,10))
#drawer=Limason.Limason(Coords2D(1080,1920), 60, 10, field_size=Coords2D(300,300),border=False, center = Coords2D(150,150), radius=50, point=Coords2D(150,150))
#drawer=ExpoCircle.ExpoCircle(Coords2D(1080,1920), 60, 20, field_size=Coords2D(300,300),border=False, points_no = 300, power = p, iters = 300)

#drawer=LongExpoCircle.LongExpoCircle(Coords2D(1920,1080), 60, 10, field_size=Coords2D(300,300),border=False, points_no = 300, min_power = 0.1, max_power = 2, delta_power = 0.002)
#drawer=LongExponentCircle.LongExponentCircle(Coords2D(1920,1080), 60, 10, field_size=Coords2D(300,300),border=False, points_no = 300, min_base = 0.85, max_base = 1.15, delta_base = 0.0002)

#this is for long #drawer.generate_video([Coords2D(1920,1080)])
'''
for p in [1.0164,1.0188,1.0208,1.023,1.0258]:
    drawer=ExponentCircle.ExponentCircle(Coords2D(1080,1920), 60, 20, field_size=Coords2D(300,300),border=False, points_no = 300, base = p, iters = 300)
    #replace for vertical!!!!!
    drawer.generate_video([Coords2D(1080,1920)])'''
    #drawer.alternative_add_audio()
'''
for degree in range(3,11):
    drawer=Mandelbrot.Mandelbrot(Coords2D(1080,1920), 60, 5, field_size=Coords2D(400,400),border=False, degree=degree,start=Coords2D(0,0))
    drawer.generate_video([Coords2D(1080,1920)])'''

#drawer=Mandelbrot.Mandelbrot(Coords2D(1080,1920), 60, 5, field_size=Coords2D(400,400),border=False, degree=2,start=Coords2D(0,0))
#drawer.generate_video_2([Coords2D(1080,1920)])


#drawer=JuliaLong.JuliaLong(Coords2D(1920,1080), 60, 6, field_size=Coords2D(500,500),border=False, degree=7)


#drawer=BurningJuliaLong.BurningJuliaLong(Coords2D(1920,1080), 60, 6, field_size=Coords2D(400,400),border=False, degree=5)
#drawer.generate_video_3([Coords2D(1920,1080)])


#drawer=LongGameOfLifeDrawer.LongGameOfLifeDrawer(Coords2D(1920,1080), 1800, 15, field_size=Coords2D(100,100),border=True)
#drawer=Methuselahs.Methuselahs(Coords2D(1080,1920), 6, 10, field_size=Coords2D(30,30),border=True)
#drawer=Multispiral.Multispiral(Coords2D(1080,1920), 30, 6, field_size=Coords2D(400,400),border=False)

#drawer=MarchingSquares.MarchingSquares(Coords2D(1920,1080), 120, Coords2D(1000,1000),5,False,150,base_color=(0,100,0),line_color=(255,155,255))
#drawer=Voronoi.Voronoi(Coords2D(1080,1920), 20, Coords2D(300,300),20,True,500)

#coagulation: {"births":[3,7,8],"stable":[2,3,5,6,7,8]}
#maze: {"births":[3],"stable":[1,2,3,4,5]}
#stains B3678/S235678
#cities B45678/S2345
#variations=[{"births":[4,5,6,7,8],"stable":[2,3,4,5]},{"births":[4,5,6,7,8],"stable":[2,3,4,5]},{"births":[4,5,6,7,8],"stable":[2,3,4,5]},{"births":[3,6,7,8],"stable":[2,3,5,6,7,8]},{"births":[3,7,8],"stable":[2,3,5,6,7,8]},{"births":[3],"stable":[1,2,3,4,5]}]
#drawer = MultiGameOfLife.MultiGameOfLife(size=Coords2D(1080,1920),rate=150,field_size=Coords2D(200,200), border=True, agents=[{"births":[3],"stable":[1,2,3,4,5]} for _ in range(random.randint(5,10))])
#points = 11
'''drawer = Pendulums.Pendulums(size=Coords2D(1080,1920),rate=30,field_size=Coords2D(700,700),
                                         border=True,
                             stick_lengths = [random.randint(1,5)*(110/points) for i in range(points-1)],
                             rules=[0 if j==0 else random.randint(1,5) for j in range(points)])'''

#drawer=ExperimentJuliaLong.ExperimentJuliaLong(Coords2D(1920,1080), 60, 6, field_size=Coords2D(400,400),border=False, degree=2)
#drawer.generate_video_3([Coords2D(1920,1080)])
'''for i in (Coords2D(-0.046930339512069305,-0.29630650217854126),Coords2D(-0.06257378601609241,-0.3950753362380551),Coords2D(-0.11448539722592688,0.5889763100685984),Coords2D(-0.16278407722857832,-0.4727592877996584),Coords2D(-0.17918397477265013,0.46679021324860087),Coords2D(-0.21502076972718015,0.5601482558983211),Coords2D(-0.30902284494603255,0.5143003804212674),Coords2D(-0.32556815445715664,-0.9455185755993168),Coords2D(-0.3581249699028723,-1.0400704331592485),Coords2D(-0.35836794954530027,0.9335804264972017),Coords2D(-0.490813591723832,-0.09540449768827236),Coords2D(-0.5248472231924057,0.6037676641782177),Coords2D(-0.7216649318895578,0.8301805382450492),Coords2D(0.003490481287456626,-0.19996953903127826),Coords2D(0.06511363089143135,0.18910371511986335),Coords2D(0.1312118057981014,-0.15094191604455445),Coords2D(0.1509419160445544,0.13121180579810146),Coords2D(0.18879611731495125,0.23314378843709122),Coords2D(0.19681770869715212,-0.2264128740668317),Coords2D(0.377354790111386,0.32802951449525364),Coords2D(0.6535062985480412,0.25085756468171017),Coords2D(0.6618630029195218,-0.22789770812000967),Coords2D(0.981627183447664,0.1908089953765448),Coords2D(1.0998324646720303,0.019197647081011862)):
    drawer=ExperimentJulia.ExperimentJulia(Coords2D(1080,1920), 60, 3, field_size=Coords2D(400,400),border=False, degree=2,c=i)
    drawer.generate_video_3([Coords2D(1080,1920)])'''
'''for i in range(2,11):
    drawer=ExperimentMandelbrot.ExperimentMandelbrot(Coords2D(1080,1920), 60, 3, field_size=Coords2D(400,400),border=False, degree=i)
    drawer.generate_video_3([Coords2D(1080,1920)])'''

#drawer= Levy.Levy(Coords2D(1080,1920), 3, 4, field_size=Coords2D(990, 1210),border=True,angle=90,max_iterations=12)
drawer= LongLevyByAngle.LongLevyByAngle(Coords2D(1920,1080), 3, 4, field_size=Coords2D(1600, 1080),border=True,max_iterations=12,verbose=False)
drawer.generate_video_3([Coords2D(1920,1080)])
#drawer.alternative_add_audio()

