import random
import GameOfLifeDrawer
import Drawer
import BallDrawer
import PolyLineDrawer
from Coords2D import Coords2D
import DragonCurve

height=1920
width=800

init_state=[[0 for _ in range(200)] for _ in range(200)]
for i in range(95,105):
    for j in range(95,105):
        init_state[i][j]=random.randint(0,1)

drawer = GameOfLifeDrawer.GameOfLifeDrawer(Coords2D(1080,1920),60,8,
                                           Coords2D(200,200), True,
                                           births=[3,7,8],stables=[2,3,5,6,7,8],initial_state=init_state)
#drawer = Drawer.Drawer((600,1000),10,1,(20,20))
#drawer=BallDrawer.BallDrawer(Coords2D(1080,1920), 60, Coords2D(500,700),20,True,100)
#drawer=PolyLineDrawer.PolyLineDrawer(Coords2D(800,1920), 10, 10, Coords2D(20,20),True)
#drawer=DragonCurve.DragonCurve(Coords2D(1080,1920), 60, 30, field_size=Coords2D(30,30),border=True,init_point=Coords2D(5,10))
drawer.generate_video([Coords2D(1080,1920)])