#ToDo: Randomisierters Setzen von Spielsteinen/ Events + Startposition einlesen der Spielfiguren
#ToDo: Setzen der Visualierungen der Events (z.B. Feuer)
#ToDo: Auslesen der Spielfeldgröße und übergeben an GameField Objekt
from enum import Enum

class Cell_Tag(Enum):
    IMPASSABLE = 'X'
    BURNT = 'B'
    FLOODED = 'F'

class Cell:
    def __init__(self, properties=None):
        if properties is None:
            properties = set()
        self.properties = properties

    def add_property(self, property_name):
        self.properties.add(property_name)

    def remove_property(self, property_name):
        self.properties.discard(property_name)

    def has_property(self, property_name):
        return property_name in self.properties

class GameField:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.figures = {}  # Dictionary to store the positions of figures
        self.events = {}  # Dictionary to store the positions of events
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def add_property(self, position, property_name):
        x, y = position
        self.grid[y][x].add_property(property_name)

    def remove_property(self, position, property_name):
        x, y = position
        self.grid[y][x].remove_property(property_name)

    def visualize(self):
        for row in self.grid:
            for cell in row:
                if cell.has_property(Cell_Tag.IMPASSABLE):
                    print(Cell_Tag.IMPASSABLE.value, end=" ")
                elif cell.has_property(Cell_Tag.FLOODED):
                    print(Cell_Tag.FLOODED.value, end=" ")
                elif cell.has_property(Cell_Tag.BURNT):
                    print(Cell_Tag.BURNT.value, end=" ")
                else:
                    print(".", end=" ")
            print()

    def add_figure(self, figure): 
        if figure.position not in self.figures:
            self.figures[figure.position] = figure
        else:
            print("Position already occupied!")

    def add_event(self, position, event):
        self.events[position] = event

    def move_figure(self, current_position, new_position): 
        if current_position in self.figures:
            figure = self.figures[current_position]
            del self.figures[current_position]
            figure.position = new_position
            self.figures[new_position] = figure
            if new_position in self.events:
                self.events[new_position].trigger()
        else:
            print("No game piece at this position!")