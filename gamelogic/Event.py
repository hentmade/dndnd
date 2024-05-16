class Event:
    def __init__(self,position,size=1):
        self.position = position
        self.size=size
        self.triggerd = False


    def trigger(self): 
        if not self.triggered:
            print("Event triggered")
            self.triggered=True


class Trap(Event):
    def __init__(self,position,size):
        super().__init__(position,size)

    def trigger(self): 
        if not self.triggered:
            print("Trap triggered")
            self.triggered=True

class Ambush(Event):
    def __init__(self,position,size):
        super().__init__(position,size)

    def trigger(self): 
        if not self.triggered:
            print("Ambush triggered")
            self.triggered=True


