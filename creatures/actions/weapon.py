# Base class for weapons
# Types: crush, poison, 
# 10 is amount of damage attempted.  Consumes energy
# Opponent can defend (which also consumes energy)

# power is max damage that can be inflicted. power used is subtracted from energy
# E.g. if power is 20, you can cause up to 20 damage if successful, but cost of using weapon is 20 energy

class Weapon():
    def __init__(self, type, power):
        self.type = type        # claw, jaws, poison, venom
        self.power = power      # integer value - 

    def __str__(self):
        return self.type + ":" + str(self.power)