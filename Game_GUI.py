from typing import Tuple
from typing import Optional, Dict
from GameField import *
from Cell import *
from Figure import *
from Event import *
from Item import *
from Map import *
from GUI import *
from PositionDetection import *
from ImageTransformer import *
from GitterErkennung import *
import mouse
import mss
import os


#following code is the call for the GUI in game.py
if __name__ == "__main__":
    app = Application(30,40)
    app.mainloop()
    