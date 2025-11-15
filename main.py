import GameOfLifeDrawer
import Drawer
import BallDrawer
import PolyLineDrawer
from Coords2D import Coords2D
import DragonCurve

height=1920
width=800

#drawer = GameOfLifeDrawer.GameOfLifeDrawer(Coords2D(600,1000),10,10, Coords2D(20,20), True)
#drawer = Drawer.Drawer((600,1000),10,1,(20,20))
#drawer=BallDrawer.BallDrawer(Coords2D(800,1920), 5, Coords2D(100,100),10,True,100)
#drawer=PolyLineDrawer.PolyLineDrawer(Coords2D(800,1920), 10, 10, Coords2D(20,20),True)
drawer=DragonCurve.DragonCurve(Coords2D(800,1920), 20, 30, field_size=Coords2D(3,3),border=True,init_point=Coords2D(1,2))
drawer.generate_video([Coords2D(800,1920),Coords2D(600,1080)])