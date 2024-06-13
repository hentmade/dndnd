#from Feld import *
from GitterErkennung import *
import cv2 


class Spielfeld:
    #def defines functions of class
    def __init__(self, name, age):
        self.name = name
        self.age = age

        list = []
        image = cv2.imread("Encounter-7-b3b93e2a-scaled.webp")
        GitterErkennung(list,image)
        

spielfeld  = Spielfeld("one",2)
#list.append(Feld(1))
print("Hello there")