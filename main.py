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
import Cesaro
import TSquare
import HSquare
import Spiral
import LineSquare
import MonteCarlo
import PointyDraw
import Rose

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
#drawer=DragonCurve.DragonCurve(Coords2D(1080,1920), 60, 30, field_size=Coords2D(30,30),border=True,init_point=Coords2D(5,10))
#drawer= Koch.Koch(Coords2D(1080,1920), 3, 1, field_size=Coords2D(400,400),border=True,side=1,max_iterations=7)
#drawer=Gosper.Gosper(Coords2D(1080,1920), 30, 700, field_size=Coords2D(20,20),border=True,init_point=Coords2D(0,10))
#drawer= Levy.Levy(Coords2D(1080,1920), 3, 4, field_size=Coords2D(990, 1210),border=True,max_iterations=15)
#drawer= Cesaro.Cesaro(Coords2D(1080,1920), 3, 1, field_size=Coords2D(1080,1080),border=False,max_iterations=7)
#drawer=TSquare.TSquare(Coords2D(1080,1920), 30, 2, field_size=Coords2D(1080,1080),border=False,max_iterations=8)
#drawer=HSquare.HSquare(Coords2D(1080,1920), 30, 2, field_size=Coords2D(1080,1080),border=False,max_iterations=8)
#drawer=Spiral.Spiral(Coords2D(1080,1920), 30, 10, field_size=Coords2D(100,100),border=True)
#drawer=LineSquare.LineSquare(Coords2D(1080,1920), 30, 30, field_size=Coords2D(500,500),border=False,side=5)
#drawer=PointyDraw.PointyDraw(Coords2D(1080,1920), 30, 100, field_size=Coords2D(40,40),border=False)
drawer=Rose.Rose(Coords2D(1080,1920), 30, 100, field_size=Coords2D(200,200),border=False,k=1/6)
'''
radius = 50 * 0.9
first_point = Coords2D(5, 95)
second_point = first_point + Coords2D(0, -radius)
third_point = first_point + Coords2D(radius, -radius)
fourth_point = first_point + Coords2D(radius, 0)
fifth_point = fourth_point + Coords2D(radius, -radius)
sixth_point = fourth_point + Coords2D(radius, 0)
seventh_point=second_point + Coords2D(0, -radius)
eighth_point=third_point + Coords2D(0, -radius)
ninth_point=fifth_point + Coords2D(0, -radius)
drawer.add_config([first_point,second_point,third_point,fourth_point],0.1)
drawer.add_config([fifth_point,sixth_point,fourth_point,third_point],0.1)
drawer.add_config([eighth_point,third_point,second_point,seventh_point],0.1)
drawer.add_config([ninth_point,fifth_point,third_point,eighth_point],0.1)
'''
drawer.generate_video([Coords2D(1080,1920)])