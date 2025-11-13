import GameOfLifeDrawer
import Drawer
import BallDrawer
from Coords2D import Coords2D

height=1920
width=800

#drawer = GameOfLifeDrawer.GameOfLifeDrawer(Coords2D(600,1000),10,10, Coords2D(20,20), True)
#drawer = Drawer.Drawer((600,1000),10,1,(20,20))
drawer=BallDrawer.BallDrawer(Coords2D(800,1920), 5, Coords2D(100,100),10,True,100)
drawer.generate_video([Coords2D(800,1920),Coords2D(600,100)])