class Event:
    def __init__(self,position,size=1):
        self.position = position
        self.size=size

    def trigger(self): 
        print("Event triggered")


class Trap(Event):
    def __init__(self,position,size):
        super().__init__(position,size)

    def trigger(self): 
        print("Trap triggered!")

class Ambush(Event):
    def __init__(self,position,size):
        super().__init__(position,size)

    def trigger(self): 
        print("Ambush triggered!")


