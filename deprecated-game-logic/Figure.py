from enum import Enum

class Figure_Tag(Enum):
    PLAYER = 'P'
    ALLY = 'A'
    ENEMY = 'E'
    OBJECT = 'O'

class Figure:
    id_counters = {tag: 0 for tag in Figure_Tag}
    def __init__(self, name,tag, position):
        self.name = name
        self.tag = tag
        self.position = position
        Figure.id_counters[tag] += 1
        self.id = f"{tag.value}{Figure.id_counters[tag]:03d}"
        #ToDo: Eine Figur kann noch weitere Werte haben, beispielsweise Lebenspunkte?

    def move(self, new_position):
        self.position = new_position