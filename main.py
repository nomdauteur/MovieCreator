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

#drawer= Levy.Levy(Coords2D(1080,1920), 3, 4, field_size=Coords2D(990, 1210),border=True,max_iterations=15)
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
#drawer=MarchingSquares.MarchingSquares(Coords2D(1080,1920), 20, Coords2D(1000,1000),5,False,200,base_color=(0,100,0),line_color=(255,155,255))
#drawer=GrowingBallDrawer.GrowingBallDrawer(Coords2D(1080,1920), 60, Coords2D(500,500),32,False,100)
#drawer=Gosper.Gosper(Coords2D(1080,1920), 30, 512, field_size=Coords2D(20,20),border=True,init_point=Coords2D(0,10))
#drawer=DragonCurve.DragonCurve(Coords2D(1080,1920), 60, 128, field_size=Coords2D(30,30),border=True,init_point=Coords2D(5,10))

drawer=Limason.Limason(Coords2D(1080,1920), 60, 10, field_size=Coords2D(300,300),border=False, center = Coords2D(150,150), radius=50, point=Coords2D(150,150))
drawer.generate_video([Coords2D(1080,1920)])
#drawer.alternative_add_audio()