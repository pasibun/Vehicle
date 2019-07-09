from ..Hexapod.hexapod import Hexapod

hexy = Hexapod()

print("walk forward")
hexy.walk(offset=25, swing=25)

print("walk backward")
hexy.walk(offset=25, swing=-25)
