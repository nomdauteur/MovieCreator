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
import LongLevyByPoints
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

#drawer=ExperimentJuliaLong.ExperimentJuliaLong(Coords2D(1920,1080), 60, 6, field_size=Coords2D(400,400),border=False, degree=4)
#drawer.generate_video_3([Coords2D(1920,1080)])
'''for i in (Coords2D(-0.05724269861296344,0.2944881550342992),Coords2D(-0.0954044976882724,0.490813591723832),Coords2D(-0.15643446504023104,-0.9876883405951377),Coords2D(-0.20601522996402172,0.3428669202808449),Coords2D(-0.25172815641993485,-0.31085838458278847),Coords2D(-0.3942047444998303,1.0269384691469219),Coords2D(-0.48480962024633756,-0.8746197071393954),Coords2D(-0.5332905822709714,-0.9620816778533351),Coords2D(-0.5665418824010597,0.9428840307723236),Coords2D(-0.8301805382450491,-0.7216649318895582),Coords2D(0.015707165793554818,-0.8998629256407522),Coords2D(0.2866943596362403,-0.7468643411977613),Coords2D(0.2930113390114411,0.8509667180393852),Coords2D(0.32253115459077036,-0.8402223838474816),Coords2D(0.35812496990287246,1.0400704331592485),Coords2D(0.3942047444998304,-1.0269384691469219),Coords2D(0.45282574813366316,0.39363541739430435),Coords2D(0.4635342674190487,-0.7714505706319011),Coords2D(0.56731114535959,-0.19534089267429403),Coords2D(0.7564148604794535,-0.26045452356572535),Coords2D(0.7901506724761101,-0.12514757203218488),Coords2D(0.9876883405951377,-0.1564344650402311),Coords2D(0.9998476951563913,0.01745240643728351),Coords2D(1.0864571746546514,-0.1720779115442542)):
    drawer=ExperimentJulia.ExperimentJulia(Coords2D(1080,1920), 60, 3, field_size=Coords2D(400,400),border=False, degree=4,c=i)
    drawer.generate_video_3([Coords2D(1080,1920)])'''
'''for i in range(2,11):
    drawer=ExperimentMandelbrot.ExperimentMandelbrot(Coords2D(1080,1920), 60, 3, field_size=Coords2D(400,400),border=False, degree=i)
    drawer.generate_video_3([Coords2D(1080,1920)])'''
init_0=Coords2D.make_regular_polygon(5,Coords2D(990/2,1210/2),990*0.2)
init=[init_0[i] for i in [0,2,4,1,3,0]]
filename="Levy_pentagram"

drawer= Levy.Levy(Coords2D(1080,1920), 3, 4, field_size=Coords2D(990, 1210),border=True,angle=90,max_iterations=12,init_state=init,filename=filename)
drawer.generate_video_3([Coords2D(1080,1920)])
#drawer= LongLevyByAngle.LongLevyByAngle(Coords2D(1920,1080), 3, 4, field_size=Coords2D(1600, 1080),border=True,max_iterations=12,verbose=False)
#drawer= LongLevyByPoints.LongLevyByPoints(Coords2D(1920,1080), 3, 4, field_size=Coords2D(1600, 1080),border=True,angle=90,max_iterations=10,verbose=False)
#drawer.generate_video_3([Coords2D(1920,1080)])
#drawer.alternative_add_audio()

