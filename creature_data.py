from settings import *

class CreatureData():
    def __init__(self):
        self.id = 0
        self.type = ""
        self.size = 0
        self.age = 0 
        self.alertness = INITIAL_ALERTNESS 
        self.energy = INITIAL_ENERGY 
        self.damage = 0 
        self.bite_size = 0

        self.angle = 0
        self.position = 0
        self.velocity = 0
        self.acceleration = 0

    def __str__(self):
        return self.type + " id=" + self.id + " size=" + str(self.size) + " age=" + str(self.age) + " energy=" + str(self.energy) + " damage=" + str(self.damage) + " alertness=" + str(self.alertness)
