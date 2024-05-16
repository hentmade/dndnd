#ToDo: 
#   - Festlegen, was es für ein Event ist und was dann passiert --> Vererbung?
#   - Event nach Triggerung entfernen

class Event:
    def __init__(self, name):
        self.name = name

    def trigger(self): 
        print("Event triggered:", self.name)

        